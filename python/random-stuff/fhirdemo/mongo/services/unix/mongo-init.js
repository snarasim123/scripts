db.createUser(
        {
            user: "engineer",
            pwd: "P@55w0rd",
            roles: [
                {
                    role: "readWrite",
                    db: "pipelineprod"
                }
            ]
        }
);
db.auth('root', 'password');
db = db.getSiblingDB('pipelineprod')
db.createCollection("AETNAClaims");
db.createCollection("AETNAEligibility");
db.createCollection("AETNASummary");
db.createCollection("patientsFHIR");
