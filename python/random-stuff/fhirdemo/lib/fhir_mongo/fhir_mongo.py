from lib.mongo_docker.mongo import MongoDB, DEFAULT_MONGO_IMAGE
from lib.mongo_docker.docker_alt import Docker, DockerException


class FhirMongo:
    def __init__(self):
        mongo_inst = MongoDB()
        mongo_inst.create_collection("AETNAClaims")
        mongo_inst.create_collection("AETNAEligibility")
        mongo_inst.create_collection("AETNASummary")
        mongo_inst.create_collection("patientsFHIR")
