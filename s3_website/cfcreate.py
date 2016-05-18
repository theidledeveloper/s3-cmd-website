import logging
import log
import helper
import command_runner


REQUIRED_ATTRIBUTES = ['s3_bucket', 's3_endpoint', ]
ACTION = 'CloudFront creation'


def set_command_line_options(subparsers):
    """
    Command line options for CloudFront distribution creation

    :param subparsers: argparse - The parser object
    """

    parser = subparsers.add_parser('cfcreate',
                                   description='Create the CloudFront'
                                               ' distribution for the s3'
                                               ' website',
                                   add_help=False,
                                   )

    parser.set_defaults(func=main)


@helper.required_configuration(REQUIRED_ATTRIBUTES)
def main(**kwargs):
    """
    Create a CloudFront distribution fronting an s3 website

    :param **kwargs -
        args: argparse - Arguments required for the website info
        s3_website_config: dict - Configuration for the website creation
    """

    logger = logging.getLogger(log.ROOT_LOGGER_NAME)
    logger.debug('Executing %s' % ACTION)

    args = kwargs['args']
    s3_website_config = kwargs['s3_website_config']

    s3_cmd_config = args.s3_cmd_config
    access_key = args.access_key
    secret_key = args.secret_key

    cname = helper.get_configuration_attribute('cloudfront_cname',
                                               s3_website_config)
    comment = helper.get_configuration_attribute('cloudfront_comment',
                                                 s3_website_config)
    root_object = helper.get_configuration_attribute('cloudfront_root_object',
                                                     s3_website_config)

    s3_bucket = helper.add_s3_prefix(s3_website_config.s3_bucket)
    s3_endpoint = s3_website_config.s3_endpoint

    logger.info("Creating CloudFront distribution '%s'" % s3_bucket)
    command = ['cfcreate', ]

    if cname:
        command.extend(['--cf-add-cname=%s' % cname],)
    if comment:
        command.extend(['--cf-comment=%s' % comment],)
    if root_object:
        command.extend(['--cf-default-root-object=%s' % root_object],)

    command.extend([s3_bucket], )

    return command_runner.run(logger=logger,
                              command=command,
                              operation=ACTION,
                              s3cmd_config_path=s3_cmd_config,
                              access_key=access_key,
                              secret_key=secret_key,
                              region=s3_endpoint,
                              )
