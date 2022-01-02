import * as cdk from '@aws-cdk/core'
import { HostedZone, IHostedZone } from '@aws-cdk/aws-route53'

export function getFootwedgeHostedZone(scope: cdk.Construct): IHostedZone {
  return HostedZone.fromHostedZoneAttributes(scope, 'FootwedgeHostedZone', {
    hostedZoneId: 'Z0842942IYF0MEQKCNQ1',
    zoneName: 'footwedge.io',
  })
}
