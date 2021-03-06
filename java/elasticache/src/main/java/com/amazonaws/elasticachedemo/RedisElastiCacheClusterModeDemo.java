/* 
 * 
 * Copyright 2021 Amazon.com, Inc. or its affiliates.  All Rights Reserved.
 * SPDX-License-Identifier: MIT-0
 * 
 */
package com.amazonaws.elasticachedemo;

import io.lettuce.core.RedisURI;
import io.lettuce.core.cluster.RedisClusterClient;
import io.lettuce.core.cluster.api.StatefulRedisClusterConnection;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Date;
import java.util.Iterator;
import java.util.Properties;
import java.util.concurrent.ExecutionException;

//import redis.clients.jedis.*;
//import redis.clients.jedis.params.SetParams;

/**
 * This class demonstrates how to use Amazon ElastiCache for Redis 
 * in cluster mode using the Jedis client.
 */
public class RedisElastiCacheClusterModeDemo {
	
	/** The properties object to hold the config. */
	private Properties properties = null;
	
	/** The Redis cluster host name. */
	private String redisHost = null;
	private String redisPassword = null;
	
	/** The Redis cluster port. */
	private int redisPort = 0;
	
	/** The cache-expiry value (in seconds). */
	private int cacheExpiryInSecs = 0;
	
	/**
	 * The flag that denotes whether cache needs to be flushed or not on shutdown.
	 */
	private boolean cacheFlushOnShutdown = false;
	
	/** The client shutdown timeout value (in seconds). */
	private int clientTimeoutInSecs = 0;
	
	/** The number of auto-generated key-value entries. */
	private int numberOfAutoGeneratedEntries = 0;
	
	/** The Jedis Cluster object. */
//	private JedisCluster jedisCluster = null;
	RedisClusterClient redisClient = null;
	StatefulRedisClusterConnection<String, String> conn = null;

	/**
	 * Constructor performing initialization.
	 *
	 * @throws IOException Signals that an I/O exception has occurred.
	 */
	public RedisElastiCacheClusterModeDemo() throws IOException {
		initialize();
	}

	/**
	 * Loads the properties from the config file and starts the Jedis client.
	 *
	 * @throws IOException Signals that an I/O exception has occurred.
	 */
	private void initialize() throws IOException {
		loadProperties();
		startClient();
	}

//	private JedisPoolConfig initPoolConfig(){
//		JedisPoolConfig poolConf = new JedisPoolConfig();
//		poolConf.setMaxTotal(12);
//        /* maximum active connections
//            Redis Enterprise can handle significantly more connections so make this number high
//            If using threads 2-3x the thread count is probably a safe rule of thumb
//            be sure to return connections to the pool
//        */
//		poolConf.setMaxIdle(12);
//        /* The maximum number of connections that should be kept in the idle pool if isPoolSweeperEnabled() returns false.
//           Connections start getting closed here if idle if you have long running idle connections consider matching setMaxTotal
//        */
//		poolConf.setMinIdle(4);
//        /* The minimum number of established connections that should be kept in the pool at all times.
//           If using threads 1.25-1.5x the number of threads is safe
//           This will ensure that connections are kept to the back end so they will recycle quickly
//        */
//		poolConf.setTestOnBorrow(false);
//        /* when true - send a ping before when we attempt to grab a connection from the pool
//           Generally not recommended as while the PING command (https://redis.io/commands/PING) is relatively lightweight
//           if there is much borrowing happening this can increase traffic if the number of operations per connection is low
//        */
//		poolConf.setTestOnReturn(false);
//        /* when true - send a ping upon returning a pool connection
//           I cannot imagine a scenario where this would be useful
//        */
//		poolConf.setTestWhileIdle(false);
//        /* when true - send ping from idle resources in the pool
//           Again the ping is not expensive
//           Recommend setting this to true if you have a firewall between client and server that disconnects idle TCP connections
//           Also common issue on the cloud with load balancers (https://aws.amazon.com/blogs/aws/elb-idle-timeout-control/)
//        */
//		poolConf.setMaxWaitMillis(60000);
//        /* set max timeout in milliseconds for write operations
//           default is -1 which means wait forever
//           Tune this carefully - often a good idea to slightly exceed your redis SLOWLOG settings,
//           so you can view what is taking so long (https://redis.io/commands/slowlog)
//        */
//		poolConf.setTestOnCreate(false);
//        /*
//        The above ??
//         */
//		return poolConf;
//	}

	/**
	 * Loads properties from the config file.
	 *
	 * @throws IOException Signals that an I/O exception has occurred.
	 */
	private void loadProperties() throws IOException {
		System.out.println("Reading config file...");
		properties = new Properties();
		FileInputStream fis = new FileInputStream(new File(System.getProperty("CONFIG_FILE_NAME")));
		properties.load(fis);
		redisHost = properties.getProperty("REDIS_CLUSTER_ENDPOINT_HOSTNAME");
		redisPassword = properties.getProperty("REDIS_PASS");

		redisPort = Integer.parseInt(properties.getProperty("REDIS_CLUSTER_ENDPOINT_PORT"));
		cacheExpiryInSecs = Integer.parseInt(properties.getProperty("REDIS_CACHE_EXPIRY_IN_SECS"));
		cacheFlushOnShutdown = Boolean.parseBoolean(properties.getProperty("REDIS_CACHE_FLUSH_ON_SHUTDOWN"));
		clientTimeoutInSecs = Integer.parseInt(properties.getProperty("REDIS_CLIENT_TIMEOUT_IN_SECS"));
		numberOfAutoGeneratedEntries = Integer.parseInt(properties.getProperty("NUMBER_OF_AUTO_GENERATED_ENTRIES"));
		fis.close();
		System.out.println("Completed reading config file.");
	}

	/**
	 * Starts the Jedis client to connect in cluster mode.
	 *
	 * @throws IOException Signals that an I/O exception has occurred.
	 */
	private void startClient() throws IOException {
		System.out.println("Initializing Redis client...");
		System.out.println("Host..."+redisHost+"redisPort..."+redisPort+"redisPassword..."+redisPassword);
		RedisURI redisURI = RedisURI.Builder.redis("<<Redis Server primary endpoint>>", 6379).withSsl(true).withVerifyPeer(false).build();
		redisClient  = RedisClusterClient.create(redisURI);
		conn = redisClient.connect();

		System.out.println("Completed initializing Redis client.");
	}


	/**
	 * Stops the Jedis client.
	 */
	private void stopClient() {
		System.out.println("Shutting down Redis client...");
//		jedisCluster.close();
		redisClient.shutdown();
		conn.close();
		System.out.println("Completed shutting down Redis client.");
	}

	/**
	 * Upserts cache entries - loops through and calls the upsertCacheEntry method.
	 *
	 * @param keyPrefix the key prefix
	 * @param valuePrefix the value prefix
	 * @param checkExists the check exists
	 * @throws InterruptedException the interrupted exception
	 * @throws ExecutionException the execution exception
	 */
//	private void upsertCacheEntries(String keyPrefix, String valuePrefix, boolean checkExists)
//			throws InterruptedException, ExecutionException {
//		for (int i = 1; i <= numberOfAutoGeneratedEntries; i++) {
//			upsertCacheEntry("Name" + i, "Value" + i, false);
//		}
//	}

	/**
	 * Upsert cache entry - adds if not present; else updates based on the key.
	 *
	 * @param key the key
	 * @param value the value
	 * @param checkExists the check exists
	 * @throws InterruptedException the interrupted exception
	 * @throws ExecutionException the execution exception
	 */
	// private void upsertCacheEntry(String key, String value, boolean checkExists)
	// 		throws InterruptedException, ExecutionException {
	// 	boolean valueExists = false;
	// 	if (checkExists && (getCacheValue(key) != null)) {
	// 		valueExists = true;
	// 	}
	// 	String result = jedisCluster.set(key, value, (new SetParams()).ex(cacheExpiryInSecs));
	// 	if (result.equalsIgnoreCase("OK")) {
	// 		if (checkExists) {
	// 			if (valueExists) {
	// 				System.out.println("Updated = {key=" + key + ", value=" + value + "}");
	// 			} else {
	// 				System.out.println("Inserted = {key=" + key + ", value=" + value + "}");
	// 			}
	// 		} else {
	// 			System.out.println("Upserted = {key=" + key + ", value=" + value + "}");
	// 		}
	// 	} else {
	// 		System.out.println("Could not upsert key '" + key + "'");
	// 	}
	// }

	/**
	 * Deletes a random cache entry; uses the key-prefix and generates the full key
	 * randomly.
	 *
	 * @param keyPrefix the key prefix
	 * @throws InterruptedException the interrupted exception
	 * @throws ExecutionException the execution exception
	 */
	// private void deleteRandomCacheEntry(String keyPrefix) throws InterruptedException, ExecutionException {
	// 	deleteCacheEntry(keyPrefix + getRandomInteger(1, numberOfAutoGeneratedEntries));
	// }

	/**
	 * Deletes the cache entry for the specified key.
	 *
	 * @param key the key
	 * @throws InterruptedException the interrupted exception
	 * @throws ExecutionException the execution exception
	 */
	private void deleteCacheEntry(String key) throws InterruptedException, ExecutionException {
//		Long result = jedisCluster.del(key);
//		if (result.longValue() == 1L) {
//			System.out.println("Deleted key '" + key + "'");
//			System.out.println("Testing delete...");
//			getCacheValue(key);
//			System.out.println("Completed testing delete.");
//		} else {
//			System.out.println("Could not delete key '" + key + "'");
//		}
	}

	/**
	 * Flushes the cache.
	 *
	 * @throws InterruptedException the interrupted exception
	 * @throws ExecutionException the execution exception
	 */
	private void flushCache() throws InterruptedException, ExecutionException {
		boolean flushSucceeded = true;
		long startTime = (new Date()).getTime();
		conn.sync().flushall();

	}

	/**
	 * Gets the specified cache value.
	 *
	 * @param key the key
	 * @return the cache value
	 */
	private String getCacheValue(String key) {
		System.out.println("..getCacheValue" );
		long startTime = (new Date()).getTime();
		String value = conn.sync().get(key);
		long endTime = (new Date()).getTime();
		if (value != null) {
			System.out.println("Retrieved value='" + value + "' for key= '" + key + "' in " + (endTime - startTime)
					+ " millisecond(s).");
		} else {
			System.out.println("Key '" + key + "' not found.");
		}
		return value;
	}

	/**
	 * Perform shutdown - flush the cache and stop the Jedis client.
	 *
	 * @throws InterruptedException the interrupted exception
	 * @throws ExecutionException the execution exception
	 */
	private void shutdown() throws InterruptedException, ExecutionException {
		if (cacheFlushOnShutdown) {
			flushCache();
		}
		stopClient();
	}

	
	/**
	 * The main method performs the following,
	 * 1. Reads the config file.
	 * 2. Instantiates the Jedis client to connect in cluster mode.
	 * 3. Upserts the specified number of key-values in the cache.
	 * 4. Prints the value of a random key in the range.
	 * 5. Deletes the key-value entry for a random key in the range.
	 * 6. Flushes the cache (if enabled).
	 * 7. Shuts down the Jedis client.
	 *
	 * @param args the arguments
	 * @throws IOException Signals that an I/O exception has occurred.
	 * @throws InterruptedException the interrupted exception
	 * @throws ExecutionException the execution exception
	 */
	public static void main(String[] args) throws IOException, InterruptedException, ExecutionException {
		String key = args[0];
		RedisElastiCacheClusterModeDemo redisElastiCacheClusterModeDemo = new RedisElastiCacheClusterModeDemo();
		//"defaultTenantId:977b3823-9f0d-225f-cd56-6b1d224cf72d:tid:977b3823-9f0d-225f-cd56-6b1d224cf72d:miss:configurationCache:auto_download_packages:devices"

		String retval = redisElastiCacheClusterModeDemo.getCacheValue(key);
		System.out.println("Value for fixed key :"+retval);
		redisElastiCacheClusterModeDemo.shutdown();
	}
}
