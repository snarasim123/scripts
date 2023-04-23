package testcontainers.data.mongo;

import com.mongodb.client.*;
import lombok.*;
import org.bson.Document;
import org.bson.conversions.Bson;


import java.util.ArrayList;
import java.util.List;

@Getter

@NoArgsConstructor

public class MongoClientHelper {

    private String Uri;
    private String CollectionName;
    private String DbName;
    private MongoCollection<Document> currentCollection;
    private MongoDatabase mongodb;

    MongoClientHelper(String uri, String collectionName, String dbName){
        this.Uri = uri;
        this.CollectionName = collectionName;
        this.DbName = dbName;
    }

    //call after changing the db or collection name in the class
    public void reset(){
        init();
    }

    //get connection to the db and get the collection
    public void init(){
        MongoClient mongoClient =  MongoClients.create(Uri);
        mongodb = mongoClient.getDatabase(DbName);
        currentCollection = mongodb.getCollection(CollectionName);
    }


    //from current collection
    public List<Document> getAllDocs() {
        MongoIterable<Document> docsIterable = currentCollection.find();
        MongoCursor<Document> docIterator = docsIterable.iterator();
        List<Document> docs = new ArrayList<>();
        while(docIterator.hasNext()){
            Document doc = docIterator.next();
            docs.add(doc);
        }
        return docs;
    }

    public List<Document> getCurrentCollection(Bson filter) {
        MongoIterable<Document> docsIterable = currentCollection.find(filter);
        MongoCursor<Document> docIterator = docsIterable.iterator();
        List<Document> docs = new ArrayList<>();
        while(docIterator.hasNext()){
            Document doc = docIterator.next();
            docs.add(doc);
        }
        return docs;
    }



    public List<String> getAllCollectionNames(){
        MongoIterable<String> collNames = mongodb.listCollectionNames();
        MongoCursor<String> colIter = collNames.iterator();
        List<String> collections = new ArrayList<String>();
        if(colIter.hasNext()){
            String col = colIter.next();
            System.out.println(col);
            collections.add(col);
        }
        return collections;
    }

}
