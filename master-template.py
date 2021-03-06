# -*- python -*-
# ex: set filetype=python:

# This is a template for a buildbot master.cfg.
# Use the `./generate_config` script will take in this template and a
# configuration file to generate a full configuration.

from buildbot.plugins import *
import os

# This is the dictionary that the buildmaster pays attention to.
# Do not change this line.
c = BuildmasterConfig = {}

def get_builders() -> list:
  """
  Get the list of builders for this buildbot.
  This method will be replaced by ./generate_config.
  """
  pass

def get_workers() -> list:
  """
  Get the list of builders for this buildbot.
  This method will be replaced by ./generate_config.
  """
  pass

def get_github_incoming_webhooks() -> list:
  """
  Get the list of GitHub incoming webhooks for this buildbot.
  This method will be replaced by ./generate_config.
  """
  pass

def get_github_status_comment_pushes() -> list:
  """
  Get the list of GitHub-related buildbot services.
  This method will be replaced by ./generate_config.
  """
  pass

def get_github_change_hook_dialect() -> dict:
  """
  Get the github change_hook_dialects dictionary.
  This method will be replaced by ./generate_config.
  """
  pass

def get_hostname() -> str:
  """
  Get the hostname for the buildbot instance.
  This method will be replaced by ./generate_config.
  """
  pass

########################################################################
# These lines are template lines used by generate_config to generate
# buildbot lines.
# No need to modify by default.
########################################################################

def template_create_step(factory, name: str, command: str) -> None:
  factory.addStep(steps.ShellCommand(
    name=name,
    command=command))

def template_create_builder(name: str, repourl: str, workernames: List[str]):
  factory = util.BuildFactory()
  factory.addStep(steps.Git(repourl=repourl, mode='incremental'))

  # generate_config will replace this with step lines
  template_create_step_placeholder(factory, ..., ...)

  return util.BuilderConfig(
    name=name,
    workernames=workernames,
    factory=factory
  )

def template_create_worker(name: str, password: str) -> None:
  worker.Worker(name, password)

def template_github_incoming_webhook(name: str, description: str, builders: List[str], filter_project: Optional[str]):
  return schedulers.AnyBranchScheduler(
    name = name,
    reason = description,
    builderNames = builders,
    change_filter = util.ChangeFilter(
      project=filter_project
    ) if filter_project is not None else None
  )

def template_github_comment_push(token: str, context: str, builders: List[str]):
  return reporters.GitHubCommentPush(token=token,
                                 context=context,
                                 postURLs=False,
                                 startDescription='Build started.',
                                 endDescription='Build done.',
                                 builders=builders)

def template_github_status_push(token: str, context: str, builders: List[str]):
  return reporters.GitHubStatusPush(token=token,
                                 context=context,
                                 postURLs=False,
                                 startDescription='Build started.',
                                 endDescription='Build done.',
                                 builders=builders)

def template_github_change_hook_dialect(secret: str):
  return {
    'secret': secret,
    'pullrequest_ref': 'direct'
  }

########################################################################
# No need to modify the lines below this.
########################################################################

# Pull some environment variables
BUILDBOT_ADMIN_PORT = int(os.environ["BUILDBOT_ADMIN_PORT"])
BUILDBOT_COMMS_PORT = int(os.environ["BUILDBOT_COMMS_PORT"])

# Workers
c['workers'] = get_workers()

# Builders
c['builders'] = get_builders()

# Schedulers
c['schedulers'] = [
  schedulers.ForceScheduler(name="force",
                            builderNames=["runtests"])
]
c['schedulers'] += get_github_incoming_webhooks()

# Services for status/comment reporting, etc.
c['services'] = []
c['services'] += get_github_status_comment_pushes()

# Add buildbot communication port
c['protocols'] = {'pb': {'port': BUILDBOT_COMMS_PORT}}

# minimalistic config to activate new web UI
# change_hook_dialects enables the github incoming webhooks
c['buildbotURL'] = f"http://{get_hostname()}:{BUILDBOT_ADMIN_PORT}/"

c['www'] = dict(port=BUILDBOT_ADMIN_PORT,
                plugins=dict(waterfall_view={}, console_view={}, grid_view={}),
                change_hook_dialects={
                  'github': get_github_change_hook_dialect()
                }
)
