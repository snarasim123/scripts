package testcontainers.data.mongo.configuration;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.Configuration;
import org.springframework.data.mongodb.MongoDbFactory;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.SimpleMongoClientDbFactory;
import org.springframework.data.mongodb.repository.config.EnableMongoRepositories;
import testcontainers.data.mongo.repository.CustomerRepository;


@Configuration
@ComponentScan(basePackages = "testcontainers.data.mongo")
@EnableMongoRepositories(basePackageClasses = CustomerRepository.class)
public class MongoDataConfig {
    @Value("${spring.data.mongodb.uri}")
    private String mongoUri;

    @Bean
    public MongoDbFactory mongoDbFactory() {
        //https://docs.mongodb.com/manual/reference/connection-string/
        SimpleMongoClientDbFactory factory = new SimpleMongoClientDbFactory(mongoUri);
        return factory;
    }
    @Bean
    public MongoTemplate mongoTemplate() throws Exception {
        MongoTemplate mongoTemplate = new MongoTemplate(mongoDbFactory());
        return mongoTemplate;
    }

}