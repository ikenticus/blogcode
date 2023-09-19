static Map<String, Map<String, Object>> projectPipeConfig() {
    def pipeConfig = [
        "terraform-show-locks": [
            "description": "Display the terraform locks currently in the AWS Account",
            "repoName": "jenkins-devops",
            "projectType": "pipeline",
            "branchPattern": "*/main",
            "scriptPath": "jobs/ci/terraform-show-locks/Jenkinsfile",
            "parameters": {
                choiceParam("ACCOUNT", ["production", "staging"], "Which AWS Account to Check")
                stringParam("REGION", "us-east-1", "")
            },
        ],
        "terraform-unlock": [
            "description": "Display the terraform locks currently in the AWS Account",
            "repoName": "jenkins-devops",
            "projectType": "pipeline",
            "branchPattern": "*/main",
            "scriptPath": "jobs/ci/terraform-unlock/Jenkinsfile",
            "parameters": {
                choiceParam("ACCOUNT", ["production", "staging"], "Which AWS Account to Check")
                stringParam("REGION", "us-east-1", "")
                stringParam("LOCK", "", "Full DynamoDB Lock Path")
            },
        ],
    ]
    return pipeConfig as Map<String, Map<String, Object>>
}
