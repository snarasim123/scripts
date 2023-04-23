package testcontainers.data.mongo;


import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoDatabase;
// import com.mongodb.client.MongoCollection;

// import org.bson.Document;
// import org.slf4j.Logger;
// import org.slf4j.LoggerFactory;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.Network;

import java.util.Optional;

public class MongoContainer {

    private static final int MONGO_PORT = 27017;
    private static final String MONGO_IMAGE = "mongo:4.0.8";

    private static MongoClient mongoClient;
    private static MongoDatabase db;

    private static Optional<String> endpointURI= Optional.empty();
    private static Optional<String> ip = Optional.empty();
    private static Integer port=0;

    // private static final Logger log = LoggerFactory.getLogger(MongoContainer.class);
    


    public MongoContainer() {
        final Network network = Network.newNetwork();
        final GenericContainer m1 = new GenericContainer(MONGO_IMAGE)
                    .withNetwork(network)
                    .withNetworkAliases("M1")
                    .withExposedPorts(MONGO_PORT)
                    .withCommand("--replSet rs0 --bind_ip localhost,M1");

        final GenericContainer m2 = new GenericContainer(MONGO_IMAGE)
                    .withNetwork(network)
                    .withNetworkAliases("M2")
                    .withExposedPorts(MONGO_PORT)
                    .withCommand("--replSet rs0 --bind_ip localhost,M2");

        final GenericContainer m3 = new GenericContainer(MONGO_IMAGE)
                .withNetwork(network)
                .withNetworkAliases("M3")
                .withExposedPorts(MONGO_PORT)
                .withCommand("--replSet rs0 --bind_ip localhost,M3");

        m1.start();
        m2.start();
        m3.start();

        try {
            m1.execInContainer("/bin/bash", "-c", "mongo --eval 'printjson(rs.initiate({_id:\"rs0\","
                    + "members:[{_id:0,host:\"M1:27017\"}]}))' " + "--quiet");
            m1.execInContainer("/bin/bash", "-c",
            "until mongo --eval \"printjson(rs.isMaster())\" | grep ismaster | grep true > /dev/null 2>&1;"
            + "do sleep 1;done");
        } catch (final Exception e) {
            throw new IllegalStateException("Failed to initiate rs.", e);
        }

        endpointURI = Optional.of("mongodb://" + m1.getContainerIpAddress() + ":" + m1.getFirstMappedPort());
        mongoClient = MongoClients.create(endpointURI.get());
        db = mongoClient.getDatabase("testdb");
        ip = Optional.of(m1.getContainerIpAddress());
        port = m1.getFirstMappedPort();

    }
    public Optional<String> getURI(){
        return endpointURI;
    }
    public MongoClient getMongoClient() {
        return mongoClient;
    }
    public Optional<String> getIp(){
        return ip;
    }
    public Integer getPort(){
        return port;
    }

}
