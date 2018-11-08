import boto3


def main():
  client = boto3.client('cognito-idp')

  poot_name = 'test-hoge'

  # ユーザープールの作成
  user_pool = _create_user_pool(client, poot_name)

  # アプリクライアントの作成
  _create_user_pool_app_client(client, user_pool)

  # TOTPを利用したMFAを有効にする
  _set_user_pool_mfa_config(client, user_pool)

  _create_user(client, user_pool, 'hoge', 'hogeHoge7!')


def _create_user_pool(client, pool_name):
  response = client.create_user_pool(
    PoolName=pool_name,
    Policies={
      'PasswordPolicy': {
        'MinimumLength': 8,
        'RequireUppercase': True,
        'RequireLowercase': True,
        'RequireNumbers': True,
        'RequireSymbols': True
      }
    },
    # LambdaConfig={
    #   'PreSignUp': 'string',
    #   'CustomMessage': 'string',
    #   'PostConfirmation': 'string',
    #   'PreAuthentication': 'string',
    #   'PostAuthentication': 'string',
    #   'DefineAuthChallenge': 'string',
    #   'CreateAuthChallenge': 'string',
    #   'VerifyAuthChallengeResponse': 'string',
    #   'PreTokenGeneration': 'string',
    #   'UserMigration': 'string'
    # },
    # AutoVerifiedAttributes=[
    #   'phone_number'|'email',
    # ],
    # AliasAttributes=[
    #   'phone_number'|'email'|'preferred_username',
    # ],
    # UsernameAttributes=[
    #   'phone_number'|'email',
    # ],
    # SmsVerificationMessage='string',
    # EmailVerificationMessage='string',
    # EmailVerificationSubject='string',
    # VerificationMessageTemplate={
    #   'SmsMessage': 'string',
    #   'EmailMessage': 'string',
    #   'EmailSubject': 'string',
    #   'EmailMessageByLink': 'string',
    #   'EmailSubjectByLink': 'string',
    #   'DefaultEmailOption': 'CONFIRM_WITH_LINK'|'CONFIRM_WITH_CODE'
    # },
    # SmsAuthenticationMessage='string',
    MfaConfiguration='OFF',
    # DeviceConfiguration={
    #   'ChallengeRequiredOnNewDevice': True|False,
    #   'DeviceOnlyRememberedOnUserPrompt': True|False
    # },
    # EmailConfiguration={
    #   'SourceArn': 'string',
    #   'ReplyToEmailAddress': 'string'
    # },
    # SmsConfiguration={
    #   'SnsCallerArn': 'string',
    #   'ExternalId': 'string'
    # },
    # UserPoolTags={
    #   'string': 'string'
    # },
    AdminCreateUserConfig={
      'AllowAdminCreateUserOnly': False,
      'UnusedAccountValidityDays': 7,
      # 'InviteMessageTemplate': {
      #     'SMSMessage': 'string',
      #     'EmailMessage': 'string',
      #     'EmailSubject': 'string'
      # }
    },
    # Schema=[
    #   {
    #     'Name': 'string',
    #     'AttributeDataType': 'String'|'Number'|'DateTime'|'Boolean',
    #     'DeveloperOnlyAttribute': True|False,
    #     'Mutable': True|False,
    #     'Required': True|False,
    #     'NumberAttributeConstraints': {
    #       'MinValue': 'string',
    #       'MaxValue': 'string'
    #     },
    #     'StringAttributeConstraints': {
    #       'MinLength': 'string',
    #       'MaxLength': 'string'
    #     }
    #   },
    # ],
    # UserPoolAddOns={
    #   'AdvancedSecurityMode': 'OFF'|'AUDIT'|'ENFORCED'
    # }
  )
  return response


def _create_user_pool_app_client(client, user_pool):
  user_pool_id = user_pool['UserPool']['Id']
  user_pool_name = user_pool['UserPool']['Name']
  response = client.create_user_pool_client(
    UserPoolId=user_pool_id,
    ClientName=f'{user_pool_name}-client',
    # GenerateSecret=True|False,
    RefreshTokenValidity=30,
    # ReadAttributes=[
    #   'string',
    # ],
    # WriteAttributes=[
    #   'string',
    # ],
    # ExplicitAuthFlows=[
    #   'ADMIN_NO_SRP_AUTH'|'CUSTOM_AUTH_FLOW_ONLY'|'USER_PASSWORD_AUTH',
    # ],
    # SupportedIdentityProviders=[
    #   'string',
    # ],
    # CallbackURLs=[
    # 'string',
    # ],
    # LogoutURLs=[
    #   'string',
    # ],
    # DefaultRedirectURI='string',
    # AllowedOAuthFlows=[
    #   'code'|'implicit'|'client_credentials',
    # ],
    # AllowedOAuthScopes=[
    #   'string',
    # ],
    # AllowedOAuthFlowsUserPoolClient=True|False,
    # AnalyticsConfiguration={
    #   'ApplicationId': 'string',
    #   'RoleArn': 'string',
    #   'ExternalId': 'string',
    #   'UserDataShared': True|False
    # }
  )
  return response


def _set_user_pool_mfa_config(client, user_pool):
  user_pool_id = user_pool['UserPool']['Id']
  response = client.set_user_pool_mfa_config(
    UserPoolId=user_pool_id,
    # SmsMfaConfiguration={
    #   'SmsAuthenticationMessage': 'string',
    #   'SmsConfiguration': {
    #     'SnsCallerArn': 'string',
    #     'ExternalId': 'string'
    #   }
    # },
    SoftwareTokenMfaConfiguration={
      'Enabled': True # True|False
    },
    MfaConfiguration='ON' # 'OFF'|'ON'|'OPTIONAL'
  )
  return response


def _create_user(client, user_pool, user_name, password):
  user_pool_id = user_pool['UserPool']['Id']
  response = client.admin_create_user(
    UserPoolId=user_pool_id,
    Username=user_name,
    # UserAttributes=[
    #   {
    #     'Name': 'string',
    #     'Value': 'string'
    #   },
    # ],
    # ValidationData=[
    #   {
    #     'Name': 'string',
    #     'Value': 'string'
    #   },
    # ],
    TemporaryPassword=password,
    # ForceAliasCreation=True|False,
    MessageAction='SUPPRESS' # 'RESEND'|'SUPPRESS',
    # DesiredDeliveryMediums=[
    #   'SMS'|'EMAIL',
    # ]
  )
  return response

if __name__ == '__main__':
  main()
