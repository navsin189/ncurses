## Jenkins-SonarQube Integration

In any programming languages there are sets of rules to be followed such as naming conventions of methods and variables, hierarchy and so on. I usually write python scripts for automation and sometime to play with APIs using web frameworks. Python follows PEP-8 (might got changed) but I never follow the same but you guys, don't be like me.
There are some linters that iterate through the scripts and let you know what to change according to the standard convention but that's all, there's nothing about vulnerability. Here comes our saviour **SonarQube**.
> **Definition:**

- *SonarQube*: It is a self-managed, automatic code review tool that systematically helps you deliver *Clean Code*. **Clean Code** is the standard for all code that results in secure, reliable, and maintainable software therefore, writing clean code is essential to maintaining a healthy codebase.

> **Let's try it**

- Install SonarQube server.
- I'm using official docker image of SonarQube.

```
> sudo docker run -d -p 9000:9000 --name sonarqube --network automation sonarqube:lts

# here's the output
> sudo docker ps | grep sonarqube
8caf46873b3d   sonarqube:lts           "/opt/sonarqube/dock…"   38 hours ago   Up 2 hours   0.0.0.0:8081->9000/tcp, :::8081->9000/tcp              sonarqube
# I used 8081 port of my local machine instead of 9000
# You can use whatever you want.
# -p <local_machine_port>:<sonarqube_server_port> 
# By default sonarqube runs on 9000
```
- go to http://127.0.0.1:9000/
- Enter admin as user and password then login.
- Update the password.
- Create a new Project
- While creating project, choose manually as project type.

> **Now the server is up but how will the scripts get scanned?**

- Download SonarQube scanner(use docker image).
```
docker run \
    --rm \
    --name sonarqube_scanner
    --network automation
    -e SONAR_HOST_URL="http://sonarqube:9000" \
    -e SONAR_SCANNER_OPTS="-Dsonar.projectKey=${YOUR_PROJECT_KEY}" \
    -e SONAR_TOKEN="myAuthenticationToken" \
    -v "${YOUR_REPO}:/usr/src" \
    sonarsource/sonar-scanner-cli
# network tag value should be same as the sonarqube server container.
# So that containers can talk to each other via their names.
# ${YOUR_PROJECT_KEY} means your newly created project name on sonarqube server
# myAuthenticationToken is the secret toekn you got for the new project.
# ${YOUR_REPO} means path to directory where your scripts resides
```
- Here's what I ran
```
sudo docker run \
    --rm \
    --name sonarqube_scanner \
    --network automation \
    -e SONAR_HOST_URL="http://sonarqube:9000" \
    -e SONAR_SCANNER_OPTS="-Dsonar.projectKey=test_project" \
    -e SONAR_TOKEN="sqp_1279d8e0313d04f1089aad5ca4e312944779ae42" \
    -v ./docker_web:/usr/src \
    sonarsource/sonar-scanner-cli

# output (last 10 lines)

INFO: ANALYSIS SUCCESSFUL, you can find the results at: http://sonarqube:9000/dashboard?id=test_project
INFO: Note that you will be able to access the updated dashboard once the server has processed the submitted analysis report
INFO: More about the report processing at http://sonarqube:9000/api/ce/task?id=AY75WTusk3cDwBn9ccWY
INFO: Analysis total time: 3.462 s
INFO: ------------------------------------------------------------------------
INFO: EXECUTION SUCCESS
INFO: ------------------------------------------------------------------------
INFO: Total time: 4.925s
INFO: Final Memory: 26M/100M
INFO: ------------------------------------------------------------------------
Check your project in server, it have the code review for your scripts.
```

> **Integration with CI/CD**
>> **Why?**

What we did above is manual tasks and is not preferable when working with teams where everyone's changes are in GitHub. To automate the process, CI/CD tools come into the picture where the famous one's are:
- Jenkins(one of the oldest automation tool)
- GitHub Actions

For now, we will move with Jenkins and its setup.
- Install Jenkins(I used docker image)
```
sudo docker pull jenkins/jenkins:jdk17
sudo docker run -d --name jenkins -p 8080:8080 --network automation jenkins/jenkins:jdk17
```
-go to http:/127.0.0.1:8080/
-it will ask for password and let you know from where to get it.
```
sudo docker exec jenkins cat /var/jenkins_home/secrets/initialAdminPassword
```
- install suggested plugins
- continue as admin
- you will get the dashboard. Now on left panel menu, click on Manage Jenkins(http://127.0.0.1:8080/manage/).
- Go to plugin → Available plugins and search for 'Sonarqube Scanner for Jenkins' then install it.
- Again go to Manage Jenkins → Tools → SonarQube Scanner installations 

- Name it *scanner* then select install automatically --> it'll show install from Maven Central --> select the version --> I choose latest one.
- Now, go to your sonarqube server UI → Click on user Icon → My Account → Security and under it create new token of user type.
- Copy the token value
- On Manage Jenkins → Credentials → System → Global Credentials → Add Credentials
- Kind should be Secret text. Scope is Global. Paste the token in Secret field. ID and Description can be given by you.
- On Manage Jenkins → System → SonarQube Servers → Check the Env Variables checkbox then add server. Give a name. URL should be http://sonarqube:9000 and server authentication token must have newly created credentials ID.

- Create new Job on Jenkins
- From dashboard → New Item → Freestyle Project → under Source Code Management, select GIT and then fill out required details such as URL and Branch specifier.
- Under Build Environment select Prepare SonarQube Scanner environment and select none as auth token.
- Under Build Step, select Execute SonarQube Scanner.
- Under Analysis Properties
  - sonar.projectKey=test_project
  - soonar.sources=.
  - sonar.login=<project_token>
- You can check it is similar to what we passed to scanner cli docker container as a argument.
- Click on Save then Build Now
- After successful build, the project on sonarqube server have the reports ready for you. 

> **Jenkins Pipeline**

Pipeline adds a powerful set of automation tools onto Jenkins, supporting use cases that span from simple continuous integration to comprehensive CD pipelines.
- create new item and select pipeline project
-  under configure go to pipeline and paste the following there
```
pipeline {
    agent any

    stages {
        stage('checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/navsin189/ncurses.git'
            }
        }
        stage('SonarQube Test'){
            steps {
                sh 'sonar-scanner -Dsonar.projectKey=test_project  -Dsonar.sources=. -Dsonar.host.url=http://sonarqube:9000 -Dsonar.login=project_token'
            }
        }
    }
}
```
- Build Now

- Here's another version of pipeline that creates project on the fly in SonarQube
```
pipeline {
    agent any
    environment {
        // Define SonarQube server configuration
        SONARQUBE_SCANNER_HOME = "${tool 'scanner'}/bin" // Path to SonarQube Scanner installation
    }
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/navsin189/ncurses'
            }
        }
        
        stage('SonarQube analysis') {
            steps {
                withSonarQubeEnv('SonarQube Server') {
                    sh "${SONARQUBE_SCANNER_HOME}/sonar-scanner -Dsonar.projectKey=pipeline"
                }
            }
        }
    }
    post {
        always {
            // Example post-build actions to perform regardless of the build result
            echo 'End of pipeline'
            // You can add any cleanup or final actions here
        }
    }
    
}
```
