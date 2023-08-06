import argparse
import glob
import json
import os

from ._version import __version__

PROJECT_INDEX_SIZE = 6
PROJECT_ASS_DEFAULT = "default"

TASK_INDEX_SIZE = 3
TASK_MAIN_PREFIX = "main"
TASK_ASS_SUFFIX = "ass"
TASK_MP4_SUFFIX = "mp4"
TASK_OUT_SUFFIX = "out.mp4"
TASK_ASS_REPLACE_MAIN = "REPLACE_MAIN"
TASK_CONTENTS_PREFIX = "contents"
TASK_CONTENTS_SUFFIX = "txt"
TASK_RESOLUTION_DEFAULT = 1080

CMD_INIT = "init"
CMD_START = "start"
CMD_PARSE = "parse"
CMD_SHIFT = "shift"
CMD_CONVERT = "convert"
CMD_FINALIZE = "finalize"

SPEAKER_DEFAULT = None
with open(f"{os.path.dirname(__file__)}/speaker_name_shortcuts.json") as name_shortcut_file:
    SPEAKER_NAME_SHORTCUTS = json.load(name_shortcut_file)
with open(f"{os.path.dirname(__file__)}/speaker_dialogue_shortcuts.json") as dialogue_shortcuts_file:
    SPEAKER_DIALOGUE_SHORTCUTS = json.load(dialogue_shortcuts_file)

CONTENT_COMMENT_MARKER = '#'
CONTENT_SPEAKER_CHANGE_MARKER = '%'
CONTENT_SPEAKER_LIST_MARKER = '|'
CONTENT_REPEAT_MARKER = '-'
CONTENT_DIALOGUE_MARKER = '/'


def main(parser=argparse.ArgumentParser()):
    parser.add_argument("-v", "--version", action="store_true")
    subparsers = parser.add_subparsers(dest="command")
    # init
    init_parser = subparsers.add_parser(CMD_INIT)
    init_parser.add_argument("-p", "--project", dest="init_project")
    init_parser.add_argument("-i", "--index", dest="init_index")
    init_parser.add_argument("-a", "--ass", dest="init_ass")
    # start
    start_parser = subparsers.add_parser(CMD_START)
    start_parser.add_argument("-a", "--ass", dest="start_ass")
    start_parser.add_argument("-t", "--task", dest="start_task")
    # parse
    parse_parser = subparsers.add_parser(CMD_PARSE)
    parse_parser.add_argument("-t", "--task", dest="parse_task")
    # shift
    shift_parser = subparsers.add_parser(CMD_SHIFT)
    shift_parser.add_argument("-t", "--task", dest="shift_task")
    shift_parser.add_argument("-a", "--add", dest="shift_add")
    # convert
    convert_parser = subparsers.add_parser(CMD_CONVERT)
    convert_parser.add_argument("-t", "--task", dest="convert_task")
    convert_parser.add_argument("-v", "--video", dest="convert_video")
    convert_parser.add_argument("-o", "--out", dest="convert_out")
    convert_parser.add_argument("-r", "--resolution", dest="convert_resolution")
    # finalize
    finalize_parser = subparsers.add_parser(CMD_FINALIZE)
    finalize_parser.add_argument("-t", "--task", dest="finalize_task")
    finalize_parser.add_argument("-s", "--skip", dest="finalize_skip", action="store_true")

    args = parser.parse_args()
    if args.version:
        return __version__
    elif args.command == CMD_INIT:
        cmd_init(args.init_project, args.init_index, args.init_ass)
    elif args.command == CMD_START:
        cmd_start(args.start_ass, args.start_task)
    elif args.command == CMD_PARSE:
        cmd_parse(args.parse_task)
    elif args.command == CMD_SHIFT:
        cmd_shift(args.shift_task, args.shift_add)
    elif args.command == CMD_CONVERT:
        cmd_convert(args.convert_task, args.convert_video, args.convert_out, args.convert_resolution)
    elif args.command == CMD_FINALIZE:
        cmd_finalize(args.finalize_task, args.finalize_skip)
    else:
        print(f"Unknown command: {args.command}, please see 'trysail -h' for usage details")


def cmd_init(project, index, ass):
    init_ass = ass if ass else PROJECT_ASS_DEFAULT
    init_index = int(index) if index else increment_index(get_latest_index(project, PROJECT_INDEX_SIZE))
    project_dir = get_indexed_relative_path(project, init_index, PROJECT_INDEX_SIZE)
    print(f"Initialize project <{project}> using index {init_index} and Aegisub template {init_ass} at {project_dir}")
    os.mkdir(project_dir)
    cmd_start(init_ass, None, project_dir)


def cmd_start(ass, task_index, ref_dir=None):
    start_task_index = int(task_index) if task_index else increment_index(
        get_latest_index(TASK_MAIN_PREFIX, TASK_INDEX_SIZE))
    ref_ass_file_path = get_ass_template(ass) if ass else get_indexed_relative_path(
        TASK_MAIN_PREFIX, start_task_index - 1, TASK_INDEX_SIZE, TASK_ASS_SUFFIX, ref_dir)
    replace_file_name = TASK_ASS_REPLACE_MAIN if ass else get_indexed_relative_path(
        TASK_MAIN_PREFIX, start_task_index - 1, TASK_INDEX_SIZE, TASK_MP4_SUFFIX)

    print(f"Start new subtitle task {start_task_index} using template {ref_ass_file_path}")
    new_ass_file_path = get_indexed_relative_path(TASK_MAIN_PREFIX, start_task_index,
                                                  TASK_INDEX_SIZE, TASK_ASS_SUFFIX, ref_dir)
    new_mp4_file_name = get_indexed_relative_path(TASK_MAIN_PREFIX, start_task_index,
                                                  TASK_INDEX_SIZE, TASK_MP4_SUFFIX)
    with open(ref_ass_file_path) as ref_ass_file, open(new_ass_file_path, 'w') as new_ass_file:
        for line in ref_ass_file:
            new_ass_file.writelines(line.replace(replace_file_name, new_mp4_file_name))

    new_content_file_name = get_indexed_relative_path(TASK_CONTENTS_PREFIX, start_task_index,
                                                      TASK_INDEX_SIZE, TASK_CONTENTS_SUFFIX, ref_dir)
    with open(new_content_file_name, 'w') as content_file:
        content_file.write("# title: \n")
        content_file.write("# url: \n")
        content_file.write("# comment: \n")


def cmd_parse(task_index):
    parse_task_index = int(task_index) if task_index else get_latest_index(TASK_MAIN_PREFIX, TASK_INDEX_SIZE)
    content_file_name = get_indexed_relative_path(TASK_CONTENTS_PREFIX, parse_task_index,
                                                  TASK_INDEX_SIZE, TASK_CONTENTS_SUFFIX)
    print(f"Parse task {parse_task_index} content file {content_file_name}")
    with open(content_file_name) as content_file:
        for line in content_file:
            for s in parse_line(line):
                print(s)


def cmd_shift(task_index, add_seconds):
    shift_task_index = int(task_index) if task_index else get_latest_index(TASK_MAIN_PREFIX, TASK_INDEX_SIZE)
    ass_file_name = get_indexed_relative_path(TASK_MAIN_PREFIX, shift_task_index, TASK_INDEX_SIZE, TASK_ASS_SUFFIX)
    n_time = float(add_seconds)
    with open(ass_file_name) as ass_file:
        for line in ass_file:
            if "Dialogue" in line:
                d_content = line[10:-1]
                infos = d_content.split(",")
                s_hour, s_minute, s_second = infos[1].split(":")
                e_hour, e_minute, e_second = infos[2].split(":")
                # TODO: consider increment hour
                s_second = "{:.2f}".format(float(s_second) + n_time)
                e_second = "{:.2f}".format(float(e_second) + n_time)
                infos[1] = "{}:{}:{}".format(s_hour, s_minute, s_second)
                infos[2] = "{}:{}:{}".format(e_hour, e_minute, e_second)
                new_infos = ",".join(infos)
                print("Dialogue: " + new_infos)


def cmd_convert(task_index, video_name, out_name, resolution):
    convert_task_index = int(task_index) if task_index else get_latest_index(TASK_MAIN_PREFIX, TASK_INDEX_SIZE)
    new_mp4_file_name = out_name if out_name else get_indexed_relative_path(TASK_MAIN_PREFIX, convert_task_index,
                                                                            TASK_INDEX_SIZE, TASK_MP4_SUFFIX)
    convert_resolution = int(resolution) if resolution else TASK_RESOLUTION_DEFAULT
    scale_x, scale_y = int(convert_resolution / 9 * 16), convert_resolution
    print(f"Convert {video_name} as {new_mp4_file_name}, scale={scale_x}:{scale_y}")
    os.system(f"ffmpeg -i {video_name} -vf scale={scale_x}:{scale_y} {new_mp4_file_name}")


def cmd_finalize(task_index, skip_git):
    finalize_task_index = int(task_index) if task_index else get_latest_index(TASK_MAIN_PREFIX, TASK_INDEX_SIZE)
    ass_file_name = get_indexed_relative_path(TASK_MAIN_PREFIX, finalize_task_index, TASK_INDEX_SIZE, TASK_ASS_SUFFIX)
    mp4_file_name = get_indexed_relative_path(TASK_MAIN_PREFIX, finalize_task_index, TASK_INDEX_SIZE, TASK_MP4_SUFFIX)
    out_file_name = get_indexed_relative_path(TASK_MAIN_PREFIX, finalize_task_index, TASK_INDEX_SIZE, TASK_OUT_SUFFIX)
    print(f"Finalize subtitle task {mp4_file_name} with {ass_file_name} to output {out_file_name}")
    os.system(f"ffmpeg -i {mp4_file_name} -vf ass={ass_file_name} -c:a copy {out_file_name}")
    if not skip_git:
        commit_git()


def get_ass_template(ass):
    return f"{os.path.dirname(__file__)}/template_{ass}.ass"


def get_indexed_relative_path(prefix, index, size, suffix=None, ref_dir=None):
    result = f"{prefix}-{str(index).zfill(size)}"
    if suffix:
        result = f"{result}.{suffix}"
    if ref_dir:
        result = f"{ref_dir}/{result}"
    return result


def get_latest_index(prefix, size):
    dirs = glob.glob(f"{prefix}-*")
    dirs.sort()
    if len(dirs):
        start = len(prefix) + 1
        return int(dirs[-1][start:start + size])
    return None


def increment_index(index):
    if index:
        return index + 1
    return 1


def commit_git():
    os.system("git add .")
    os.system("git commit -m 'trysail auto-commit'")
    os.system("git push")


def parse_line(line):
    global SPEAKER_DEFAULT
    if line[0] == CONTENT_COMMENT_MARKER:
        return []
    elif (line[0]) == CONTENT_SPEAKER_CHANGE_MARKER:
        SPEAKER_DEFAULT = line[1:-1]
        return []
    split_parts = line.split(CONTENT_DIALOGUE_MARKER)
    if len(split_parts) == 1:
        speakers, dialogue = SPEAKER_DEFAULT, split_parts[0]
    else:
        speakers, dialogue = split_parts
    dialogue = dialogue.replace("\n", "")  # cleanup newline character
    sentences = []
    # shortcut: /shortcut_name
    if not speakers:
        for shortcut_line in SPEAKER_DIALOGUE_SHORTCUTS[dialogue]:
            sentences.extend(parse_line(shortcut_line))
    else:
        # multiple speakers: n|m/dialogue
        for speaker_expr in speakers.split(CONTENT_SPEAKER_LIST_MARKER):
            speaker, mark, times = speaker_expr, None, 1
            # repeated sentence: n-!3/dialogue　= nansu repeats ! in the end of dialogue 3 times
            if CONTENT_REPEAT_MARKER in speaker_expr:
                speaker, rep = speaker_expr.split(CONTENT_REPEAT_MARKER)
                if not speaker:
                    speaker = SPEAKER_DEFAULT
                mark, times = rep[0], int(rep[1])
            speaker_name = SPEAKER_NAME_SHORTCUTS[speaker] if speaker in SPEAKER_NAME_SHORTCUTS else speaker
            for t in range(times):
                sentences.append(f"Dialogue: 0,,,{speaker_name},,0,0,0,,{dialogue}{mark * (t + 1) if mark else ''}")
    return sentences
