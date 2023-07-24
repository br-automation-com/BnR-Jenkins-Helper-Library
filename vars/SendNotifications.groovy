/**
 * Send notifications based on build status string
 */
def call(Map config = [buildStatus:'STARTED']) {
  // build status of null means successful
  config.buildStatus = config.buildStatus ?: 'SUCCESS'

  // Default values
  def colorName = 'RED'
  def colorCode = '#FF0000'
  def subject = "${config.buildStatus}: Job '${env.JOB_NAME} [${env.BUILD_NUMBER}]'"
  def summary = "${subject} (${env.BUILD_URL})"
  def details = '''${SCRIPT, template="groovy-html.template"}'''

  // Override default values based on build status
  if (config.buildStatus == 'STARTED') {
    color = 'YELLOW'
    colorCode = '#FFFF00'
  } else if (config.buildStatus == 'SUCCESS') {
    color = 'GREEN'
    colorCode = '#00FF00'
  } else {
    color = 'RED'
    colorCode = '#FF0000'
  }

  // Send notifications
  //hipchatSend (color: color, notify: true, message: summary)

  emailext (
      to: config.recipients,
      from: 'no-reply@br-automation.com',
      subject: subject,
      body: details,
      mimeType: 'text/html',
      recipientProviders: [[$class: 'DevelopersRecipientProvider']]
    )
}