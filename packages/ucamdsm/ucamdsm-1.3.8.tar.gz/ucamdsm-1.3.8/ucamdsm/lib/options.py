import argparse
import getpass
import json
import logging
from argparse import ArgumentParser, ArgumentTypeError

from .connection import DSMConnection
from .process import Process
from .task import Task

LOG = logging.getLogger(__name__)


class LoadFromFile(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        with values as f:
            args = json.load(f)

        for k, v in args.items():
            setattr(namespace, k, v)


class Options:
    def __init__(self):
        self.process = Process()
        self._init_parser()

    def _init_parser(self):
        """Define arguments for the CLI."""
        self.parser = ArgumentParser(description='Manage Dell Storage Manager objects via REST API.')

        self.parser.add_argument('--dsm_host',
                                 default='sc-data-ma.admin.cam.ac.uk', type=str,
                                 help='DSM hostname. Default: sc-data-ma.admin.cam.ac.uk')
        self.parser.add_argument('--dsm_port',
                                 default=3033,
                                 help='DSM port. Default: 3033')
        self.parser.add_argument('--dsm_user',
                                 type=str,
                                 help='DSM Data Collector username')
        self.parser.add_argument('--dsm_password',
                                 type=str,
                                 help='DSM Data Collector password')
        self.parser.add_argument('--is_secure',
                                 type=str2bool,
                                 default=False,
                                 help='Secure connection. Default: False')
        self.parser.add_argument('--record_config',
                                 type=str2bool,
                                 default=False,
                                 help='Record multipath and file system config details.\
                                 Default: False (do not record system config details)')
        self.parser.add_argument('--file',
                                 type=open,
                                 action=LoadFromFile,
                                 help='Read arguments from json file')

        self.subparsers = self.parser.add_subparsers(dest='subparser')

        # list dell sc objects
        self.parser_list = self.subparsers.add_parser('list',
                                                      help='List Dell SC objects. \
                                                      Example: ucamdsm --dsm_user user --dsm_password abc123 list \
                                                      --object scs')
        self.parser_list.add_argument(
            '--object',
            required=True,
            choices=['scs', 'servers', 'volumes', 'snapshots', 'volFolders', 'snapshotProfiles', 'recycledVols'])
        self.parser_list.add_argument('--output',
                                      choices=['json'],
                                      help='Format of the output. Supported formats: json')

        # delete_volume
        self.parser_delete_volume = self.subparsers.add_parser('delete_volume',
                                                               help='Delete Dell SC Volume. \
                                                               Example: ucamdsm --dsm_user user \
                                                               --dsm_password abc123 delete_volume \
                                                               --vol_wwn 12345')
        self.parser_delete_volume.add_argument('--vol_wwn',
                                               required=True,
                                               help='ID of the volume to delete. \
                                               Must be mapped to local server')
        self.parser_delete_volume.add_argument('--recycle',
                                               type=str2bool,
                                               default=True,
                                               help='Recycle the volume or delete it permanently. \
                                               Default: True (recycle the volume)')

        # replace_volume
        self.parser_replace_volume = self.subparsers.add_parser('replace_volume',
                                                                help='Clone the volume mounted on source \
                                                                mountpoint and mount it on destination mountpoint. \
                                                                Then, delete the volume was initially mounted on \
                                                                destination mountpoint. Example: ucamdsm --dsm_user \
                                                                user  --dsm_password abc123 replace_volume \
                                                                --src_mp /src --dst_mp /dst')
        self.parser_replace_volume.add_argument('--src_mp',
                                                required=True,
                                                help='Source mountpoint. Must be on local server')
        self.parser_replace_volume.add_argument('--dst_mp',
                                                required=True,
                                                help='Destination mountpoint. Must be on local server')
        self.parser_replace_volume.add_argument('--unmount_src_mp',
                                                type=str2bool,
                                                default=True,
                                                help='Optional. If False, do not unmount the source mountpoint. \
                                                      Defaults to True')

        # clone_volume
        self.parser_clone_volume = self.subparsers.add_parser('clone_volume',
                                                              help='Create a snapshot with label of a volume \
                                                              with WWN, create a view volume from the snapshot, \
                                                              then, map the view volume to local server and \
                                                              mount it on target mountpoint. Example: ucamdsm \
                                                              --dsm_user user --dsm_password abc123 clone_volume \
                                                              --vol_wwn 12345 --replay_label test1 --clone_name name \
                                                              --target_mp /target')
        self.parser_clone_volume.add_argument('--vol_wwn',
                                              required=True,
                                              help='WWN of the volume from which to create the snapshot')
        self.parser_clone_volume.add_argument('--replay_label',
                                              required=True,
                                              help='Snapshot label.')
        self.parser_clone_volume.add_argument('--clone_name',
                                              required=True,
                                              help='Name of clone volume.')
        self.parser_clone_volume.add_argument('--target_mp',
                                              required=True,
                                              help='The mountpoint that the view volume will be mounted on. \
                                              Must be on local server')

        # create_snapshot
        self.parser_create_snapshot = self.subparsers.add_parser('create_snapshot',
                                                                 help='Create a snapshot of the volume mounted on \
                                                                 a given mountpoint. Example: ucamdsm --dsm_user \
                                                                 user --dsm_password abc123 create_snapshot --mp /mp \
                                                                 --replay_label test1 --retention 5')
        self.parser_create_snapshot.add_argument('--mp',
                                                 required=True,
                                                 help='The mountpoint where the volume is mounted. \
                                                 Must be on local server')
        self.parser_create_snapshot.add_argument('--replay_label',
                                                 required=True,
                                                 help='Snapshot label')
        self.parser_create_snapshot.add_argument('--retention',
                                                 required=True,
                                                 help='Retention period of the snapshot to create, in days')

        # deleted the recycled vols whose wwns are listed in a file
        self.parser_delete_recycled_vols = self.subparsers.add_parser('delete_recycled_vols',
                                                                      help='Delete recycled volumes whose WWNs are listed in a file. \
                                                                      Example: ucamdsm --dsm_user user --dsm_password \
                                                                      abc123 delete_recycled_vols --wwns_file \
                                                                      /tmp/recycled_vols_wwns.txt')
        self.parser_delete_recycled_vols.add_argument('--wwns_file',
                                                      required=True,
                                                      help='File containing the WWNs of the recycled volumes \
                                                      to be deleted.')

        # map volume to local server
        self.parser_map_volume = self.subparsers.add_parser('map_volume',
                                                            help='Maps the volume to local server and \
                                                            mounts it on the specified mount point. \
                                                            Example: ucamdsm --dsm_user \
                                                            user --dsm_password abc123 map_volume --wwn vol_wwn \
                                                            --mp /d10')
        self.parser_map_volume.add_argument('--wwn',
                                            required=True,
                                            help='WWN of the volume to map to local server.')
        self.parser_map_volume.add_argument('--mp',
                                            required=False,
                                            help='OPTIONAL. If specified, it is the path of the mountpoint \
                                            to mount the volume on. Otherwise, no mount attempt will take place.')

        # unmap volume from local server
        self.parser_unmap_volume = self.subparsers.add_parser('unmap_volume',
                                                              help='Unmaps the volume from local server. Volume \
                                                              must be unmounted. Example: ucamdsm --dsm_user \
                                                              user --dsm_password abc123 create_snapshot --wwn vol_wwn')
        self.parser_unmap_volume.add_argument('--wwn',
                                              required=True,
                                              help='WWN of the volume to unmap from local server.')

        # clone a volume from a snapshot and mount it on a given mountpoint
        self.parser_volume_from_snapshot = self.subparsers.add_parser('volume_from_snapshot',
                                                                      help='Clone a volume from a snapshot and mount it \
                                                                      on a given mountpoint.\
                                                                      Example: ucamdsm --dsm_user \
                                                                      user --dsm_password abc123 volume_from_snapshot \
                                                                      --sid snapshot_id --rpid replay_profile_id \
                                                                      --vol_name clone_name \
                                                                      --folder_id volume_folder_id \
                                                                      --mp target_mountpoint')
        self.parser_volume_from_snapshot.add_argument('--sid',
                                                      required=True,
                                                      help='The ID of the snapshot from which to \
                                                      create the new volume.')
        self.parser_volume_from_snapshot.add_argument('--rpid',
                                                      required=True,
                                                      help='The snapshot profile to use \
                                                      for the new volume.')
        self.parser_volume_from_snapshot.add_argument('--vol_name',
                                                      required=True,
                                                      help='Name of the new volume.')
        self.parser_volume_from_snapshot.add_argument('--folder_id',
                                                      required=True,
                                                      help='The ID of the folder to locate the new \
                                                      volume in.')
        self.parser_volume_from_snapshot.add_argument('--mp',
                                                      required=True,
                                                      help='The mountpoint to mount the new volume on.')

    def parse(self, args=None):
        """Parse given arguments and execute an action accordingly."""
        result = None
        self.known, self.unknown = self.parser.parse_known_args(args)[:]

        if len(self.unknown) != 0:
            LOG.error('*WARN* Unknown args received: %s.', repr(self.unknown))
            return False

        if self.known.subparser is None or \
                self.known.subparser not in ['list', 'delete_volume',
                                             'replace_volume', 'clone_volume', 'create_snapshot',
                                             'delete_recycled_vols', 'map_volume', 'unmap_volume',
                                             'volume_from_snapshot']:
            LOG.error('No subcommand is specified (%s).', self.known.subparser)
            return False

        # Read crendential
        if self.known.dsm_user is None:
            self.known.dsm_user = input('Username: ')

        if self.known.dsm_password is None:
            self.known.dsm_password = getpass.getpass()

        # If enabled, record system config before running ucamdsm command
        if self.known.record_config:
            self.process.record_config_details()

        result = run_option(self.known.subparser, self.known)

        # If enabled, record system config after running ucamdsm command
        if self.known.record_config:
            self.process.record_config_details()

        return result


def str2bool(v):
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise ArgumentTypeError('Boolean value expected.')


def run_option(subparser, args):
    """
    Runs a ucamdsm subcommand.

    :param subparser: the subcommand to run.
    :param args: args to pass to the ucamdsm subcommand.
    :return: result of the executed subcommand.
    """
    function_switcher = {
        'list': list_object,
        'delete_volume': delete_volume,
        'replace_volume': replace_volume,
        'clone_volume': clone_volume,
        'create_snapshot': create_snapshot,
        'delete_recycled_vols': delete_recycled_vols,
        'map_volume': map_volume,
        'unmap_volume': unmap_volume,
        'volume_from_snapshot': volume_from_snapshot
    }

    subcommand_func = function_switcher.get(subparser)

    return subcommand_func(args) if subcommand_func is not None else None


def list_object(args):
    """
    List Dell SC objects.

    Example: ucamdsm --dsm_user user --dsm_password abc123 list --object scs
    """
    with DSMConnection(args.dsm_host, args.dsm_port, args.dsm_user,
                       args.dsm_password, args.is_secure) as dsm_conn:

        (result, data) = dsm_conn.run_list_object(args.object)

        if not result or data is None:
            return result

        if args.output is None:
            LOG.info('List of %s:\n%s', args.object, '\n'.join(str(item) for item in data.items()))
            return result

        if args.output == 'json':
            LOG.info('List of %s:\n%s', args.object, json.dumps(data, indent=4, sort_keys=False))

    return result


def delete_volume(args):
    """
    Example: ucamdsm --dsm_user user --dsm_password abc123 delete_volume --vol_wwn 12345
    """
    with Task(args.dsm_host, args.dsm_port, args.dsm_user, args.dsm_password, args.is_secure) as task:
        result = task.delete_volume(args.vol_wwn, recycle=args.recycle)

    if result:
        LOG.info('delete_volume(%s, recycle=%s) succeeded. Result: %s.',
                 args.vol_wwn, args.recycle, result)
    else:
        LOG.error('delete_volume(%s, recycle=%s) failed. Result: %s.',
                  args.vol_wwn, args.recycle, result)

    return result


def replace_volume(args):
    """
    Example: ucamdsm --dsm_user user --dsm_password abc123 replace_volume --src_mp /src --dst_mp /dst
    """
    with Task(args.dsm_host, args.dsm_port, args.dsm_user, args.dsm_password, args.is_secure) as task:
        result = task.replace_volume(args.src_mp, args.dst_mp, args.unmount_src_mp)

    if result:
        LOG.info('replace_volume(%s, %s, %s) succeeded. Result: %s.',
                 args.src_mp, args.dst_mp, args.unmount_src_mp, result)
    else:
        LOG.error('replace_volume(%s, %s, %s) failed. Result: %s.',
                  args.src_mp, args.dst_mp, args.unmount_src_mp, result)

    return result


def clone_volume(args):
    """
    Example: ucamdsm --dsm_user user --dsm_password abc123 clone_volume \
        --vol_wwn 12345 --replay_label test1 \
        --target_mp /target
    """
    with Task(args.dsm_host, args.dsm_port, args.dsm_user, args.dsm_password, args.is_secure) as task:
        result = task.clone_volume(args.vol_wwn, args.replay_label, args.clone_name, args.target_mp)

    if result:
        LOG.info('clone_volume(%s, %s, %s, %s) succeeded. Result: %s.',
                 args.vol_wwn, args.replay_label, args.clone_name, args.target_mp, result)
    else:
        LOG.error('clone_volume(%s, %s, %s, %s) failed. Result: %s.',
                  args.vol_wwn, args.replay_label, args.clone_name, args.target_mp, result)

    return result


def create_snapshot(args):
    """
    Example: ucamdsm --dsm_user user --dsm_password abc123 \
         create_snapshot --mp /mp --replay_label test1 --retention 5
    """
    with Task(args.dsm_host, args.dsm_port, args.dsm_user, args.dsm_password, args.is_secure) as task:
        result = task.create_snapshot(args.mp, args.replay_label, args.retention)

    if result:
        LOG.info('create_snapshot(%s, %s, %s) succeeded. Result: %s.',
                 args.mp, args.replay_label, args.retention, result)
    else:
        LOG.error('create_snapshot(%s, %s, %s) failed. Result: %s.',
                  args.mp, args.replay_label, args.retention, result)

    return result


def delete_recycled_vols(args):
    """
    Example: ucamdsm --dsm_user user --dsm_password abc123 \
         delete_recycled_vols --wwns_file /tmp/recycled_vols_wwns.txt
    """
    with Task(args.dsm_host, args.dsm_port, args.dsm_user, args.dsm_password, args.is_secure) as task:
        result = task.delete_recycled_vols(args.wwns_file)

    if result:
        LOG.info('delete_recycled_vols(%s) succeeded. Result: %s.', args.wwns_file, result)
    else:
        LOG.error('delete_recycled_vols(%s failed. Result: %s.', args.wwns_file, result)

    return result


def map_volume(args):
    """
    Example: ucamdsm --dsm_user user --dsm_password abc123 \
         map_volume --wwn 012345 --mp /d10
    """
    with Task(args.dsm_host, args.dsm_port, args.dsm_user, args.dsm_password, args.is_secure) as task:
        result = task.map_dellsc_volume(args.wwn, args.mp)

    if result:
        LOG.info('map_volume(%s, %s) succeeded. Result: %s.', args.wwn, args.mp, result)
    else:
        LOG.error('map_volume(%s, %s) failed. Result: %s.', args.wwn, args.mp, result)

    return result


def unmap_volume(args):
    """
    Example: ucamdsm --dsm_user user --dsm_password abc123 \
         unmap_volume --wwn 012345
    """
    with Task(args.dsm_host, args.dsm_port, args.dsm_user, args.dsm_password, args.is_secure) as task:
        result = task.unmap_dellsc_volume(args.wwn)

    if result:
        LOG.info('unmap_volume(%s) succeeded. Result: %s.', args.wwn, result)
    else:
        LOG.error('unmap_volume(%s) failed. Result: %s.', args.wwn, result)

    return result


def volume_from_snapshot(args):
    """
    Example: ucamdsm --dsm_user user --dsm_password abc123 \
         map_volume --sid 1234 --rpid 5678 --vol_name new_vol --folder_id 2314 --mp /d01
    """
    with Task(args.dsm_host, args.dsm_port, args.dsm_user, args.dsm_password, args.is_secure) as task:
        result = task.volume_from_snapshot(args.sid, args.rpid, args.vol_name, args.folder_id, args.mp)

    if result:
        LOG.info('volume_from_snapshot(%s, %s, %s, %s, %s) succeeded. \
            Result: %s.', args.sid, args.rpid, args.vol_name, args.folder_id, args.mp, result)
    else:
        LOG.info('volume_from_snapshot(%s, %s, %s, %s, %s) failed. \
            Result: %s.', args.sid, args.rpid, args.vol_name, args.folder_id, args.mp, result)

    return result
