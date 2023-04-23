db.createUser({user:"admin",pwd:"admin",roles: [{ role: "userAdminAnyDatabase", db: "admin" },{ role: "readWrite", db: "admin" }]});
db.createUser({user:"test",pwd:"test",roles: [{role: "root",db: "admin"}]});
db = new Mongo().getDB("pipeline");
db.createCollection('patientsFHIR', { capped: false });
// db.patient.insert([{ "item": 1 },{ "item": 2 },{ "item": 3 },{ "item": 4 },{ "item": 5 }]);