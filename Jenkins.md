# Jenkins

## 简介
pipeline脚本有两种类型：
- declarative.
- scripted.

Declarative的关键字是pipeline.

Scripted的关键字是node.

Example:
```
	pipeline {
		agent any
		stages {
			stage('Build') {
				steps {
					//...
				}
			}
			stage('Test') {
				steps {
					//...
				}
			}
		}
	}

	node {
		stage('Build') {
			//...
		}
		stage('Test') {
			//...
		}
	}
```

不管是pipeline还是node，都要有stage和steps. 

例如sh 'make'就是一个step.

### 环境变量

全局环境变量env，可以在jenkinsfile的任何地方使用。env下面包含多个变量：
- BUILD_ID
- BUILD_NUMBER
- BUILD_TAG
- BUILD_URL
- EXECUTOR_NUMBER
- JAVA_HOME
- JENKINS_URL
- JOB_NAME
- NODE_NAME
- WORKSPACE

Declarative pipeline支持environment directive，可以定义环境变量。environment directive可以定义在pipeline block或者stage block，范围不同。



动态定义环境变量 ？？

```
	environment {
		// Using returnStdout
		CC = """${sh(
				returnStdout: true,
				script: 'echo "clang"'
			)}""" 
		// Using returnStatus
		EXIT_STATUS = """${sh(
				returnStatus: true,
				script: 'exit 1'
			)}"""
	}
```

### Credentials

可以在jenkins中注册Credentials，必须指定一个有意义的Credential ID，例如 jenkins-aws-secret-key-id。注意: 该字段是可选的。如果没有指定值，Jenkins 则会分配一个全局唯一ID（GUID）值。一旦设置了credential ID，就不能再进行更改。

在pipeline中，declarative Pipeline syntax has the credentials() helper method (used within the environment directive)

example:

```
	environment {
        AWS_ACCESS_KEY_ID     = credentials('jenkins-aws-secret-key-id')
        AWS_SECRET_ACCESS_KEY = credentials('jenkins-aws-secret-access-key')
    }
```

withCredentials ???



### Parameter

Declarative Pipeline 支持自定义参数（parameters directive）. 

example:
```
	parameters {
        string(name: 'Greeting', defaultValue: 'Hello', description: 'How should I greet the world?')
    }
```

Groovy supports declaring a string with either single quotes, or double quotes, for example:
```
	def singlyQuoted = 'Hello'
	def doublyQuoted = "World"
```

Only the latter string will support the dollar-sign ($) based string interpolation, for example:
```
	def username = 'Jenkins'
	echo 'Hello Mr. ${username}'
	echo "I said, Hello Mr. ${username}"
```
Would result in:
```
Hello Mr. ${username}
I said, Hello Mr. Jenkins
```

### Failure

Declarative Pipeline supports post section which allows declaring a number of different "post conditions" such as: always, unstable, success, failure, and changed.

```
pipeline {
    agent any
    stages {
        stage('Test') {
            steps {
                sh 'make check'
            }
        }
    }
    post {
        always {
            junit '**/target/*.xml'
        }
        failure {
            mail to: team@example.com, subject: 'The Pipeline failed :('
        }
    }
}
```

Scripted Pipeline however relies on Groovy’s built-in try/catch/finally semantics for handling failures during execution of the Pipeline.


### 并行执行



agent关键字，required.

## Docker with pipeline




## groovy