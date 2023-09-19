// For now, refactoring all the manual Jobs into this MadLibs pipeline
// Hopefully, will eventually evolve to Multibranch Pipelines with Jenkinsfiles

import static projectConfig.projectPipeConfig

defaultValues = [
    "adminEmail"       : "admin@company.com",
    "githubOrg"        : "company",
    "scmCredentialsId" : "jenkins/credentials/github-userpass",
    "scriptPath"       : "Jenkinsfile",
    "shellCommand"     : "echo Hello World",
]

permissionsJob = [
    'com.cloudbees.plugins.credentials.CredentialsProvider.Create',
    'com.cloudbees.plugins.credentials.CredentialsProvider.Delete',
    'com.cloudbees.plugins.credentials.CredentialsProvider.ManageDomains',
    'com.cloudbees.plugins.credentials.CredentialsProvider.Update',
    'com.cloudbees.plugins.credentials.CredentialsProvider.View',
    'hudson.model.Item.Build',
    'hudson.model.Item.Cancel',
    'hudson.model.Item.Configure',
    'hudson.model.Item.Delete',
    'hudson.model.Item.Discover',
    'hudson.model.Item.Move',
    'hudson.model.Item.Read',
    'hudson.model.Item.Workspace',
    'hudson.model.Run.Delete',
    'hudson.model.Run.Replay',
    'hudson.model.Run.Update',
    'hudson.plugins.jobConfigHistory.JobConfigHistory.DeleteEntry',
    'hudson.scm.SCM.Tag'
]

// https://jenkinsci.github.io/job-dsl-plugin/#path/multibranchPipelineJob
def projectMultibranchPipeline(String jobName, Map<String, Object> values) {
    multibranchPipelineJob(jobName) {
        displayName(values.displayName ?: jobName)
        description(values.description ?: "Multibranch Pipeline for $jobName")

        branchSources {
            github {
                id(jobName)
                repository(values.repoName)
                repoOwner(values.githubOrg ?: defaultValues.githubOrg)
                scanCredentialsId(values.scmCredentialsId ?: defaultValues.scmCredentialsId)
                checkoutCredentialsId(values.scmCredentialsId ?: defaultValues.scmCredentialsId)

                buildForkPRHead(false)
                buildForkPRMerge(false)
                buildOriginBranch(true)
                buildOriginBranchWithPR(false)
                buildOriginPRHead(false)
                buildOriginPRMerge(true)

                includes(values.branchPattern ?: "main PR-*")
            }
        }

        factory {
            workflowBranchProjectFactory {
                scriptPath(values.scriptPath ?: defaultValues.scriptPath)
            }
        }

        orphanedItemStrategy {
            discardOldItems {
                daysToKeep(values.buildDaysToKeep ?: -1)
                numToKeep(values.buildNumToKeep ?: -1)
            }
        }

        configure {
            it / definition / lightweight(true)
        }
    }
}

// https://jenkinsci.github.io/job-dsl-plugin/#path/pipelineJob
def projectPipeline(String jobName, Map<String, Object> values) {
    pipelineJob(jobName) {
        def githubOrg = values.githubOrg ?: defaultValues.githubOrg

        // Nov2022: github-webhook trigger does NOT work for PipelineJob
        //          for triggered jobs, use Multibranch or Freestyle types
        // Webhook Log ERROR: Considering to poke <job/project>
        // Skipped <job/project> because it doesn't have a matching repository.
        triggers {
            if (values.triggerOnGitPush) {
                githubPush()
            }
            if (values.triggerOnCron) {
                cron(values.triggerOnCron) // Build periodically
            }
        }

        description(values.description ?: "Pipeline for $jobName")

        // Project parameters need to be defined here instead of Jenkinsfile
        // for FIRST run after SEED, otherwise job w/o defaultValues will FAIL
        if (values.parameters) {
            parameters(values.parameters)
        }

        if (values.jobMatrix) {
            // Establish job-based permissions on production jobs/projects
            authorization {
                blocksInheritance()
                permission('hudson.model.Item.Discover', 'GG-Staging-Jenkins-Basic')
                values.jobMatrix.forEach { String jobCall ->
                    permissions(jobCall, permissionsJob)
                }
            }
        }

        logRotator {
            daysToKeep(values.buildDaysToKeep ?: -1)
            numToKeep(values.buildNumToKeep ?: -1)
            artifactDaysToKeep(values.artifactDaysToKeep ?: -1)
            artifactNumToKeep(values.artifactNumToKeep ?: -1)
        }

        if (values.throttleMaxPerNode || values.throttleMaxTotal) {
            throttleConcurrentBuilds {
                maxPerNode(values.throttleMaxPerNode ?: 1)
                maxTotal(values.throttleMaxTotal ?: 1)
            }
        }

        if (values.repoName) {
            definition {
                cpsScm {
                    scm {
                        git {
                            remote {
                                github("${githubOrg}/${values.repoName}", "https")
                                credentials(values.scmCredentialsId ?: defaultValues.scmCredentialsId)
                            }
                            branches(values.branchPattern ?: '*/master')
                            scriptPath(values.scriptPath ?: defaultValues.scriptPath)
                            extensions {}  // required as otherwise it may try to tag the repo, which you may not want
                        }
                    }
                }
            }
        }

        configure {
            it / definition / lightweight(true)
        }
    }
}

// https://jenkinsci.github.io/job-dsl-plugin/#path/freeStyleJob
def projectFreestyle(String jobName, Map<String, Object> values) {
    job(jobName) {
        description(values.description ?: "Pipeline for $jobName")
        keepDependencies(values.keepDependencies ?: false)
        concurrentBuild(values.concurrentBuild ?: false)
        disabled(values.jobDisabled ?: false)

        triggers {
            if (values.triggerOnGitPush) {
                githubPush()
            }
            if (values.triggerOnCron) {
                cron(values.triggerOnCron) // Build periodically
            }
        }

        if (values.parameters) {
            parameters(values.parameters)
        }

        logRotator {
            daysToKeep(values.buildDaysToKeep ?: -1)
            numToKeep(values.buildNumToKeep ?: -1)
            artifactDaysToKeep(values.artifactDaysToKeep ?: -1)
            artifactNumToKeep(values.artifactNumToKeep ?: -1)
        }

        def githubOrg = values.githubOrg ?: defaultValues.githubOrg
        if (values.repoName) {
            scm {
                git {
                    remote {
                        github("${githubOrg}/${values.repoName}", "https")
                        credentials(values.scmCredentialsId ?: defaultValues.scmCredentialsId)
                    }
                    branch(values.branchPattern ?: "\${BRANCH}")
                }
            }
        }

        if (values.restrictJob) {
            label(values.restrictJob)
        }

        def shellCommand = values.shellCommand ?: defaultValues.shellCommand
        steps {
            shell(shellCommand)
            shell("echo \$GIT_COMMIT > sha_file")
            if (values.jobTriggers) {
                publishers {
                    downstreamParameterized {
                        values.jobTriggers.forEach { String jobCall, Map<String, String> params ->
                            trigger(jobCall.split(':')[0]) {
                                parameters{
                                    predefinedProps(params)
                                }
                            }
                        }
                    }
                }
            }
            buildNameUpdater {
                buildName(values.buildNameFile ?: 'sha_file')
                macroTemplate(values.buildName ?: "#\${BUILD_NUMBER}")
                fromFile(true)
                fromMacro(false)
                macroFirst(false)
            }
        }

        def notifyEmail = values.notifyEmail ?: defaultValues.adminEmail
        publishers {
            mailer("${notifyEmail}", true, true)

            // DISABLED richTextPublisher due to security concerns
            // if (values.publisherJob) {
            //     def publisherText = values.publisherText ?: values.publisherJob
            //     richTextPublisher {
            //         stableText("""<hr>
            //             <h2><a href="${JENKINS_URL}/job/${values.publisherJob}/parambuild/?SERVICE=\${ENV:SERVICE}&BUILD_ENV=\${ENV:BUILD_ENV}&AMI_NAME=\${ENV:AMI_NAME}&VERSION=\${ENV:VERSION}&BRANCH=\${ENV:PROJECT_BRANCH}">${values.publisherText}</a></h2>
            //             <hr>""")
            //         unstableText("")
            //         failedText("")
            //         abortedText("")
            //         nullAction(0)
            //         unstableAsStable(true)
            //         failedAsStable(true)
            //         abortedAsStable(true)
            //         parserName("HTML")
            //     }
            // }
        }

        wrappers {
            preBuildCleanup {
                deleteDirectories(values.deleteDirectories ?: false)
                cleanupParameter()
            }
        }

        configure {
            it / 'properties' / 'jenkins.model.BuildDiscarderProperty' {
                strategy {
                    daysToKeep(values.buildDaysToKeep ?: -1)
                    numToKeep(values.buildNumToKeep ?: -1)
                    artifactDaysToKeep(values.artifactDaysToKeep ?: -1)
                    artifactNumToKeep(values.artifactNumToKeep ?: -1)
                }
            }
            it / 'properties' / 'com.sonyericsson.rebuild.RebuildSettings' {
                autoRebuild(values.autoRebuild ?: false)
                rebuildDisabled(values.disableRebuild ?: false)
            }
        }

        // if (values.slackChannel) {
        //     def slackResponse = slackSend(
        //         iconEmoji
        //         channel: "${values.slackChannel}", color: "danger"
        //         username: "packandship", iconEmoji: ":octagonal_sign:"
        //         message: """*BUILD FAILURE* `SERVICE` for `BUILD_ENV`""")
        //     slackResponse.addReaction("thumbsup")
        // }
    }
}

projectPipeConfig().forEach { String jobName, Map<String, Object> values ->
    if (values.projectType?.startsWith('multi')) {
        projectMultibranchPipeline(jobName, values)
    } else if (values.projectType?.startsWith('pipe')) {
        projectPipeline(jobName, values)
    } else {
        projectFreestyle(jobName, values)
    }
}


