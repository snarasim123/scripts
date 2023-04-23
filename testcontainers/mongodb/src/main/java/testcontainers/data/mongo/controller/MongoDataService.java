package testcontainers.data.mongo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.stereotype.Service;
import testcontainers.data.mongo.bean.Customer;
import testcontainers.data.mongo.repository.CustomerRepository;

import java.util.List;
import java.util.Optional;


@Service
@ComponentScan(basePackages = "testcontainers.data.mongo")
public class MongoDataService {
    @Autowired
    CustomerRepository repository;

    public void run(String[] args) {
//        repository.deleteAll();
//
//		// save a couple of customers
//		repository.save(new Customer("Alice", "Smith"));
//		repository.save(new Customer("Bob", "Smith"));
//
//		// fetch all customers
//		System.out.println("Customers found with findAll():");
//		System.out.println("-------------------------------");
//		for (Customer customer : repository.findAll()) {
//			System.out.println(customer);
//		}
//		System.out.println();
//
//		// fetch an individual customer
//		System.out.println("Customer found with findByFirstName('Alice'):");
//		System.out.println("--------------------------------");
//		System.out.println(repository.findByFirstName("Alice"));
//
//		System.out.println("Customers found with findByLastName('Smith'):");
//		System.out.println("--------------------------------");
//		for (Customer customer : repository.findByLastName("Smith")) {
//			System.out.println(customer);
//		}
    }
    public boolean create( String firstname, String lastname){
		Customer c = repository.save(new Customer(firstname, lastname));
    	return true;
	}
	public Optional<List<Customer>> findAll(){
    	return Optional.of(repository.findAll());
	}
	public Optional<Customer> findByFirstName(String firstname){
		return Optional.of(repository.findByFirstName(firstname));
	}
	public Optional<List<Customer>> findByLastName(String lastname){
		return Optional.of(repository.findByLastName(lastname));
	}
	public void deleteAll(){
		repository.deleteAll();
	}
}
