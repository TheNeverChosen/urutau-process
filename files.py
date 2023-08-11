import os.path

devices={'motog200', 'pixel6'}
languages={'C', 'CPP', 'JAVA', 'KOTLIN', 'PYTHON'}
algorithms={'BINARY_TREES', 'FANNKUCH', 'FASTA', 'NBODY', 'PI_DIGITS'}
extension='.csv'
preDir='pre'
postDir='post'
qtTests=11 #ignore first

def copy_file_without_first_last(input_file, output_file):
  with open(input_file, 'r') as f:
    lines = f.readlines()
  lines = lines[1:-1]

  os.makedirs(os.path.dirname(output_file), exist_ok=True)
  with open(output_file, 'w') as f:
    f.writelines(lines)


def checkSingleFile(fileName, firstLine, lastLine, copy=False):
  if not os.path.isfile(fileName):
    print(f'File {fileName} does not exist')
    return False
  with open(fileName) as f:
    first_line = f.readline().strip('\n')
    for line in f:
      pass
    last_line = line
    ok = not((first_line==firstLine) ^ (last_line==lastLine))
    if ok:
      copy_file_without_first_last(fileName, fileName.replace(preDir, postDir, 1))
    else: print(f'File {fileName} corrupted')

    return ok
    # True: already checked and updated
    # False: corrupted (first or last line marked)


def checkAllFiles(copy=False):
  ret = True
  for dev in devices:
    for lang in languages:
      for alg in algorithms:
        for i in range(1,qtTests+1):
          fileName = f'./{preDir}/{dev}/{lang}-{alg}-{i}{extension}'
          firstLine = f'{lang}-{alg}'
          ret &= checkSingleFile(fileName, firstLine, 'fim')
  return ret


print(checkAllFiles())