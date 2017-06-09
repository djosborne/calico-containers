pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh 'make binary'
        archiveArtifacts artifacts: 'dist/calicoctl-linux-amd64'
      }
    }
  }
}
