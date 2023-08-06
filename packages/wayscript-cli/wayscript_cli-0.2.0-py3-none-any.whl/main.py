from typing import Dict, List, Tuple
from datetime import datetime
import click, ast, requests, os, json, threading, sys, html, hashlib, time
from os.path import expanduser

debug = False
verbose = False

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import socketio
socket = socketio.Client( logger=debug, engineio_logger=debug )

BASE_URL = 'https://wayscript.com'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def progress(text): return bcolors.OKBLUE + text + bcolors.ENDC
def success(text): return bcolors.OKGREEN + text + bcolors.ENDC
def fail(text): return bcolors.FAIL + text + bcolors.ENDC
def warning(text): return bcolors.WARNING + text + bcolors.ENDC

@socket.event
def connect():
    if verbose: print(success('Connected to WayScript'))

@socket.event
def connect_error(err):
    if verbose: print(fail(f'Connected to WayScript Failed: "{err}"'))

@socket.event
def disconnect():
    if verbose: print(success('Disconnected from WayScript'))

@socket.on('run error')
def run_error(err):
    print(fail(err))
    socket.disconnect()
    sys.exit(1)

@socket.on('run success')
def run_success(script_name):
    print(success(f'Running script: "{script_name}"'))

@socket.on('authenticated')
def authenticated():
    if verbose: print(success('Authenticated account with WayScript'))

@socket.on('connected to room')
def connected_to_room(room):
    if verbose: print(success(f'Connected to room: {room}'))

def _handle_message_stream(data):
    message_type = data.get('message_type', None)
    if message_type in ('message', 'print', 'code', 'error', 'warning'):
        time = data.get('timestamp', None)
        module = data.get('module', None)
        mod_category = data.get('mod_category', None)
        display_name = data.get('display_name', None)
        content = data.get('content', None)

        if time:
            dt = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f%z')
            timestamp = dt.strftime("%B %d, %Y : %H:%M:%S")
            timestamp = progress(f'[{timestamp}]')
        else: timestamp = progress(f'[N/A]')

        content = html.unescape(content).strip()

        if message_type == 'error':
            content = fail(content)
            module_name = fail(f'( {display_name} )')
        elif message_type == 'warning':
            content = warning(content)
            module_name = warning(f'( {display_name} )')
        else:
            module_name = success(f'( {display_name} )')

        if message_type == 'code' or (message_type == 'error' and mod_category == 'code'):
            content = content.split('\n')
            print(f'{timestamp} {module_name}')
            for c in content:
                print(f'      {c}')
        else:
            print(f'{timestamp} {module_name} {content}')

@socket.on('emitter update')
def emitter_update(msg_list):
    did_finish = False
    for msg, data in msg_list:
        if msg == 'finished running':
            did_finish = True

        elif msg == 'display while running':
            if verbose: print(data)
            for item in data:
                _handle_message_stream(item)
    
    if did_finish:
        print(success(f'Finished Running'))
        socket.disconnect()

def get_user_home_dir(): return expanduser('~')
def get_config_dir(): return os.path.join(get_user_home_dir(), '.ws')
def get_config_path(): return os.path.join(get_config_dir(), 'config.json')


def write_config(data):
    if not os.path.exists(get_config_dir()):
        os.makedirs(get_config_dir())

    data = json.dumps(data)
    with open(get_config_path(), 'w') as f:
        f.write(data)


def load_config():
    if not os.path.exists(get_config_path()):
        return {}
    raw_config = open(get_config_path(), 'r').read()
    config = json.loads(raw_config)
    return config


def make_request(mode, endpoint, config=None, json=None, files=None):
    if mode != 'GET' and mode != 'POST': raise Exception('Mode must be either "GET" or "POST"')
    request_func = requests.get if mode == 'GET' else requests.post

    if config is None: config = load_config()
    if not config.get('username', '') or not config.get('api_key', '' ):
        print(fail('Invalid Username or API Key. Run "wayscript configure".'))
        sys.exit(1)

    try:
        res = request_func(f'{BASE_URL}/api/{endpoint}', verify=False,
                           json=json, files=files, auth=(config['username'], config['api_key']))
    except (requests.exceptions.ConnectionError) as e:
        print(fail('Unable to connect to WayScript.'))
        sys.exit(1)

    return res


def get_current_ws_root():
    root_dir = None
    cur_dir = os.getcwd()
    while True:
        contents = os.listdir( cur_dir )
        if '.ws' in contents:
            if 'config.json' not in os.listdir( os.path.join( cur_dir, '.ws' ) ):
                root_dir = cur_dir
                break
        cur_dir, _ = os.path.split( cur_dir )
        if os.path.dirname( cur_dir ) == cur_dir: break
    return root_dir


def get_current_username():
    config = load_config()
    if not config:
        raise Exception('No user credentials found')
    
    return config.get('username', '')


def save_file_tree(root_path: str, files: List, last_pulled_at = None):
    current_username = get_current_username()
    filename = f'filecache.{current_username}.json'
    path = os.path.join(root_path, '.ws', filename)
    pulled_at = str(last_pulled_at) if last_pulled_at else str(datetime.now())
    data = { 'pulled_at': pulled_at, 'files': files }
    with open(path, 'w') as f:
        f.write(json.dumps(data, sort_keys=True, indent=2))


def get_file_cache(root_path: str) -> Tuple[datetime, List]:
    current_username = get_current_username()
    filename = f'filecache.{current_username}.json'
    path = os.path.join(root_path, '.ws', filename)
    
    if not os.path.exists(path):
        return None, []
    
    raw = ''
    with open(path, 'r') as f:
        raw = f.read()
    data = json.loads(raw) if len(raw) else {}
    pulled_at = data.get('pulled_at', None)
    if pulled_at:
        pulled_at = datetime.strptime(pulled_at, '%Y-%m-%d %H:%M:%S.%f')
    return pulled_at, data.get('files', [])


def get_user_yes_or_no(prompt):
    valid_response = None
    last_response = None
    while not valid_response:
        if last_response:
            print(f'"{last_response}" is not a valid response')
        last_response = input(prompt)
        if last_response == 'y' or last_response == 'n':
            valid_response = last_response
    return valid_response


# Traverse file tree dict and return list of file/folder nodes (with 'rel_path' added) in top down order
def process_file_tree(file_tree: Dict):
    file_dict = {k: { **v, 'uuid': k } for k, v in file_tree.items()}
    username = get_current_username()

    user_storage_roots = [file for file in file_dict.values() if file['is_storage_root'] and file['name'] == username]
    if len(user_storage_roots) != 1:
        raise Exception('Unexpected file directory returned from WayScript')

    storage_root = user_storage_roots[0]
    buffer = [(f'./{storage_root["name"]}', storage_root)] # List[Tuple[filepath, file_object]]
    files = [] # List[Tuple[filepath, file_object]]
    while len(buffer):
        (rel_path, file_obj) = buffer.pop()
        files.append({ **file_obj, 'rel_path': rel_path })

        if file_obj['is_directory']:
            children_files = [file_dict[f_id] for f_id in file_obj['children']]
            for child_file in children_files:
                new_path = f'{rel_path}/{child_file["name"]}'
                buffer.append((new_path, child_file))
    return files


def update_file_cache_for_pushes(root_dir: str, file_paths: List[str]):
    now = str(datetime.now())
    last_pulled, files = get_file_cache(root_dir)
    new_files = []
    for file_path in file_paths:
        
        adjusted_path = f'./{file_path}' if not file_path.startswith('./') else file_path
        match = [i for i, x in enumerate(files) if x['rel_path'] == adjusted_path]
        if len(match) > 0:
            index = match[0]
            files[index] = { **files[index], 'pushed_at': now }
        else:
            new_file = {'uuid': '', 'etag': '', 'rel_path': adjusted_path, 'pushed_at': now}
            new_files.append(new_file)
    
    files = files + new_files
    save_file_tree(root_dir, files, last_pulled_at=last_pulled)


def attempt_to_match_local_file_to_etag(file_path, etag):
    def _factor_of_1MB(filesize, num_parts):
        x = filesize / int(num_parts)
        y = x % 1048576
        return int(x + 1048576 - y)

    def _calc_simple_etag(path):
        data = None
        with open(path, 'rb') as f:
            data = f.read()
        return hashlib.md5(data).hexdigest()

    def _calc_multipart_etag(path, partsize):
        md5_digests = []
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(partsize), b''):
                md5_digests.append(hashlib.md5(chunk).digest())
        return hashlib.md5(b''.join(md5_digests)).hexdigest() + '-' + str(len(md5_digests))

    filesize  = os.path.getsize(file_path)
    complex_etag = etag and '-' in etag
    
    if not complex_etag:
        return _calc_simple_etag(file_path) == etag
    
    num_parts = int(etag.split('-')[1])
    partsizes = [
        8388608, # aws_cli/boto3
        15728640, # s3cmd
        _factor_of_1MB(filesize, num_parts) # Used by many clients to upload large files
    ]

    possible_partsizes = [partsize for partsize in partsizes if partsize < filesize and (float(filesize) / float(partsize)) <= num_parts]
    for partsize in possible_partsizes:
        if etag == _calc_multipart_etag(file_path, partsize):
            return True

    return False


# Compare two file lists, return new files with 'should_pull', 'is_dirty', 'was_ignored' props
def compare_files(root_path: str, old_files: List, files: List, pulled_at):
    for i, file in enumerate(files):
        if file['is_directory']:
            continue
        
        file_exists_locally = None
        local_and_remote_hash_equal = None
        local_changed_since_pull = None
        local_changed_since_push = None
        local_pushed_since_pull = None
        
        was_ignored_last_pull = any([ f['uuid'] == file['uuid'] and f.get('should_ignore', False) for f in old_files ])

        # Check file information against local file
        file_path = os.path.join(root_path, file['rel_path'])
        file_exists_locally = os.path.exists(file_path)
        if file_exists_locally:
            # Attempt to generate etag for local value and check for match
            local_and_remote_hash_equal = attempt_to_match_local_file_to_etag(file_path, file['etag'])

            statbuf = os.stat(file_path)
            last_changed_at = datetime.fromtimestamp(statbuf.st_mtime)
            
            old_match = [f for f in old_files if file['rel_path'] == f['rel_path']]
            pushed_at = old_match[0].get('pushed_at', None) if len(old_match) else None
            pushed_at = datetime.strptime(pushed_at, '%Y-%m-%d %H:%M:%S.%f') if pushed_at else None

            local_changed_since_pull = pulled_at and last_changed_at.timestamp() > pulled_at.timestamp()
            local_changed_since_push = pushed_at and last_changed_at.timestamp() > pushed_at.timestamp()
            local_pushed_since_pull = pushed_at and pulled_at and pulled_at.timestamp() < pushed_at.timestamp()

        
        files[i]['is_new'] = not file_exists_locally
        files[i]['should_pull'] = not local_and_remote_hash_equal

        local_changed_since_pull or was_ignored_last_pull
        local_is_dirty = local_changed_since_push if local_pushed_since_pull else local_changed_since_pull or was_ignored_last_pull

        file_dirty_and_different = not local_and_remote_hash_equal and local_is_dirty
        if file_dirty_and_different:
            response = get_user_yes_or_no(f'{progress(file["rel_path"])} has unpushed changes, overwrite? {success("y")}/{fail("n")}\n')
            if response == 'n':
                files[i]['should_ignore'] = True
                files[i]['should_pull'] = False
    
    return files
    

def pull_directory(files: List):
    root_dir = get_current_ws_root()
    cwd = os.getcwd()
    
    # Scope files pulled based on folder relative to WayScript root
    prefix_pattern = f'./{os.path.relpath(cwd, root_dir)}' if cwd != root_dir else ''
    path_in_context = lambda p: p.startswith(prefix_pattern) or prefix_pattern.startswith(p)
    is_path_dir = lambda p: os.path.isdir(os.path.join(root_dir, p))
    get_rep_path = lambda f: f['rel_path']

    files_to_pull = [f for f in files if not f['is_directory'] and path_in_context(f['rel_path']) and f.get('should_pull', False)]
    files_to_pull = sorted(files_to_pull, key=get_rep_path)
    folders_to_pull = [f for f in files if f['is_directory'] and path_in_context(f['rel_path']) and not is_path_dir(f['rel_path'])]
    folders_to_pull = sorted(folders_to_pull, key=get_rep_path)
    
    for folder in folders_to_pull:
        dir_path = os.path.join(root_dir, folder['rel_path'])
        os.makedirs(dir_path, exist_ok=True)
        non_rel_path = folder['rel_path'][2:] if folder['rel_path'].startswith('./') else folder['rel_path']
        print(progress('+ ') + non_rel_path + '/')

    new_files = [f for f in files_to_pull if f.get('is_new', False)]
    changed_files = [f for f in files_to_pull if not f.get('is_new', False)]
    new_files = download_files_in_parallel(new_files)
    changed_files = download_files_in_parallel(changed_files)
    
    if len(new_files) == 0 and len(changed_files) == 0 and len(folders_to_pull) == 0:
        print(f'All up to date.')
        return

    if len(folders_to_pull):
        print(f"{len(folders_to_pull)} folders added(+)")
    print(f"{len(new_files)} files added(+), {len(changed_files)} files updated(◭)")


def download_files_in_parallel(files: List[object]) -> List[object]:
    root_dir = get_current_ws_root()
    
    changed_files = []
    successfully_pulled_files = []
    def _download_file(file, retry_count = 0):
        rel_path = file['rel_path']
        try:
            res = make_request('GET', f'files/{file["uuid"]}')
            if not res or not res.ok: raise Exception('Invalid response from server.')
            file_body = res.content
            file_path = os.path.join(root_dir, rel_path)
            successfully_pulled_files.append(file)
            
            # Check one last time if the new file content is different
            if os.path.exists(file_path):
                current_data = None
                with open(file_path, 'rb') as f:
                    current_data = f.read()
                hasnt_changed = file_body == current_data
                if hasnt_changed: return

            with open(file_path, 'wb') as f:
                f.write(file_body)

            non_rel_path = file['rel_path'][2:] if file['rel_path'].startswith('./') else file['rel_path']
            pre = success('+ ') if file.get('is_new', False) else success('◭ ')
            print(pre + non_rel_path)

            changed_files.append(file)
        except Exception as e:
            # Assume the backend gave us a bad/stale file and ignore this case
            if res.status_code == 422 and res.text == 'invalid file uuid':
                successfully_pulled_files.append(file)
                return
            
            if res.status_code >= 500 and retry_count < 3:
                retry_count += 1
                time.sleep(0.25 * retry_count)
                return _download_file(file, retry_count=retry_count)
            
            non_rel_path = file['rel_path'][2:] if file['rel_path'].startswith('./') else file['rel_path']
            print(fail(f'! {non_rel_path} (failed to download)'))
        
    threads = []
    for file_obj in files:
        t = threading.Thread( target=_download_file, args=[file_obj] )
        threads.append(t)

    for t in threads: t.start()
    for t in threads: t.join()
    
    had_error = len(successfully_pulled_files) != len(files)
    if had_error:
        print(fail(f'Something went wrong pulling down your files'))
    return changed_files

@click.group()
@click.option('--debug/--no-debug', '_debug', default=False)
@click.option('--verbose/--no-verbose', '_verbose', default=False)
def cli(_debug, _verbose):
    global debug
    debug = _debug

    global verbose
    verbose = _verbose

    if debug: click.echo(warning('Debug mode is on'))
    if verbose: click.echo(warning('Verbose mode is on'))


@cli.command()
def configure():
    def_username = ''
    def_api_key  = ''
    config = load_config()
    if config:
        def_username = config.get('username', '')
        def_api_key  = config.get('api_key', '' )

    test_passed = False
    for i in range(3):
        if def_username:
            username = input(f'WayScript Username [{def_username}]: ')
            if not username: username = def_username
        else:
            username = input('WayScript Username: ')

        if def_api_key:
            disp_api_key = '****************' + def_api_key[len(def_api_key)-4:]
            api_key = input(f'WayScript API Key [{disp_api_key}]: ')
            if not api_key: api_key = def_api_key
        else:
            api_key = input('WayScript API Key: ')

        res = make_request('GET', 'user', config={ 'username': username, 'api_key': api_key })
        if res and res.ok and res.json() and res.json().get('code', None) == 200:
            test_passed = True
            break
        else: print(warning('Invalid WayScript Username or API Key. Please try again:'))

    if test_passed:
        write_config({ 'username': username, 'api_key': api_key })
        print(success('WayScript CLI configured.'))
    else:
        print(fail('Failed to configure WayScript CLI.'))
        sys.exit(1)


@cli.command()
def pull():
    root_dir = get_current_ws_root()
    if not root_dir:
        if os.listdir( os.getcwd() ):
            print(fail('Current directory is a not WayScript directory, but is also not empty. ' + \
                          'Please use an empty directory to make a new WayScript directory.'))
            sys.exit(1)
        else: 
            print(progress(f'Initializing WayScript directory at {os.getcwd()}'))
            os.makedirs('.ws', exist_ok=True)
            root_dir = get_current_ws_root()

    print('Pulling your WayScript file system...')
    res = make_request('GET', 'pull')
    if not res or res.status_code != 200:
        print(fail(f'Failed to pull WayScript files.'))
        return

    file_tree = res.json()['data']
    files = process_file_tree(file_tree)
    pulled_at, cached_files = get_file_cache(root_dir)
    files = compare_files(root_dir, cached_files, files, pulled_at = pulled_at)

    pull_directory(files)
    save_file_tree(root_dir, files)


@cli.command()
@click.argument('path', default='')
def push(path):
    wsignore = ['.ws']
    is_ignored_path = lambda path: any([ path.startswith(ptrn) for ptrn in wsignore ])
    root_dir = get_current_ws_root()
    if not root_dir:
        print(fail('Must be inside of a WayScript directory to push.'))
        sys.exit(1)
        
    cwd = os.getcwd()
    prefix_path = os.path.relpath(os.path.join(cwd, path), root_dir) if path else None

    dir_nodes = []
    file_nodes = []
    for base, dirs, files in os.walk( os.getcwd() ):
        for filename in files:
            filepath = os.path.relpath(os.path.join(base, filename), root_dir)
            if is_ignored_path(filepath): continue
            if path and not filepath.startswith(prefix_path):
                continue
            file_nodes.append(filepath)

        for directory in dirs:
            filepath = os.path.relpath(os.path.join(base, directory), root_dir)
            if is_ignored_path(filepath): continue
            if path and not filepath.startswith(prefix_path):
                continue
            dir_nodes.append(f'{filepath}/')

    pushed_files = []
    def _upload_file(filepath, dir = False, retry_count = 0):
        try:
            abs_path = os.path.join(root_dir, filepath)
            if filepath[-1] == '/': files = [('files', (f'/{filepath}', b''))]
            else: files = [('files', (f'/{filepath}', open(abs_path, 'rb').read()))]
            res = make_request('POST', 'upload-file', files=files)
            if not res or not res.ok: raise Exception('Invalid response from server.')
            pushed_files.append(filepath)
            post_message = ''

            data = res.json()
            ws_results = data.get('results', {}).get('ws', {})
            if ws_results:
                ws_modules_pushed = ws_results.get('updated_modules', [])
                if ws_modules_pushed:
                    delta_triangle = success('◭')
                    module_summary = ' '.join(ws_modules_pushed)
                    post_message = f' { delta_triangle } { module_summary }'

            if dir:
                pre = progress('← ')
                print(pre + filepath)
            else:
                pre = success('← ')
                print(pre + filepath + post_message)
        except Exception as e:
            possible_rate_limit = res.status_code == 503
            if possible_rate_limit and retry_count < 5:
                retry_count += 1
                time.sleep(retry_count * 0.25)
                return _upload_file(filepath, dir=dir, retry_count=retry_count)
            
            if res.text.startswith('ws: '):
                err = res.text.replace('ws: ', '! ')
                print(fail(err))    
            print(fail(f'! {filepath} (failed to upload)'))
            
    print(f'Uploading {len(file_nodes + dir_nodes)} files:  ')
    for filepath in dir_nodes:
        _upload_file(filepath, dir = True)
        
    threads = []
    for filepath in file_nodes:
        t = threading.Thread( target=_upload_file, args=[filepath] )
        threads.append(t)
    
    for t in threads: t.start()
    for t in threads: t.join()
    
    update_file_cache_for_pushes(root_dir, pushed_files)
    
    had_error = len(pushed_files) != (len(dir_nodes) + len(file_nodes))
    if had_error:
        print(fail(f'Something went wrong pushing some of your files'))
        sys.exit(1)
    else:
        print(f"{len(dir_nodes)} folders, {len(file_nodes)} files pushed")


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):
        try:
            if isinstance(value, str): return ast.literal_eval(value)
            elif isinstance(value, (list, tuple)): return value
            raise Exception
        except Exception as e:
            raise click.BadParameter(value)


@cli.command()
@click.argument('script_name', default='')
@click.option('--function', default=0)
@click.option('--trigger', default=-1)
@click.option('--args', cls=PythonLiteralOption, default=[])
def run(script_name, function, trigger, args):
    if trigger == -1: trigger = None

    if not script_name:
        found_ws_file = False
        cur_dir = os.getcwd()
        while True:
            contents = os.listdir( cur_dir )
            cur_dir, name = os.path.split( cur_dir )
            if '.ws' in contents: break
            if f'{name}.ws' in contents: script_name = name

        if not script_name:
            print(fail('When not inside a script directory, please specify the name of the script to run.'))
            sys.exit(1)

    config = load_config()
    
    websocket_failed = True
    # try:
    #     config = load_config()
    #     socket.connect(BASE_URL, auth=config)
    #     websocket_failed = False
    # except (socketio.exceptions.ConnectionError) as e:
    #     print(e)
    
    data = {
        'auth': config,
        'script_name': script_name,
        'args': args,
        'tree_index': function,
        'trigger_index': trigger,
    }

    if websocket_failed:
        res = make_request('POST', 'run', json=data)

        if res and res.ok and res.json() and res.json().get('code', None) == 200:
            data = {} if not res.json() else res.json().get('data', {})
            pid = None if not data else data.get('program_id', None)
            print(success(f'Running script: "{script_name}"'))
            program_link = progress(f'{BASE_URL}/edit/{pid}')
            print(f'See more output at: {program_link}')
        else:
            if res.status_code == 404:
                print(fail(f'Could not find script: "{script_name}"'))
            else:
                print(fail(f'Failed to run script: "{script_name}"'))
            sys.exit(1)
    else:
        socket.emit('auth and run', data)

if __name__ == '__main__':
    cli()
