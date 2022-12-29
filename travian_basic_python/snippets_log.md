# List of snippets of interesting code

### 1.- Error
```
	(tf_gpu_mygames) PS C:\Users\metol\Downloads> git clone https://github.com/openai/baselines
	Cloning into 'baselines'...
	remote: Enumerating objects: 3627, done.
	remote: Total 3627 (delta 0), reused 0 (delta 0), pack-reused 3627
	Receiving objects: 100% (3627/3627), 6.46 MiB | 9.65 MiB/s, done.
	Resolving deltas: 100% (2429/2429), done.
	(tf_gpu_mygames) PS C:\Users\metol\Downloads> cd .\baselines\
	(tf_gpu_mygames) PS C:\Users\metol\Downloads\baselines> pip install .
	Processing c:\users\metol\downloads\baselines
	  Preparing metadata (setup.py) ... done
	Collecting gym<0.16.0,>=0.15.4
	  Downloading gym-0.15.7.tar.gz (1.6 MB)
	     ---------------------------------------- 1.6/1.6 MB 11.0 MB/s eta 0:00:00
	  Preparing metadata (setup.py) ... done
	Requirement already satisfied: scipy in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from baselines==0.1.6) (1.6.3)
	Collecting tqdm
	  Downloading tqdm-4.64.1-py2.py3-none-any.whl (78 kB)
	     ---------------------------------------- 78.5/78.5 KB ? eta 0:00:00
	Requirement already satisfied: joblib in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from baselines==0.1.6) (0.17.0)
	Requirement already satisfied: cloudpickle in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from baselines==0.1.6) (2.2.0)
	Collecting click
	  Using cached click-8.1.3-py3-none-any.whl (96 kB)
	Collecting opencv-python
	  Downloading opencv_python-4.6.0.66-cp36-abi3-win_amd64.whl (35.6 MB)
	     ---------------------------------------- 35.6/35.6 MB 11.7 MB/s eta 0:00:00
	Requirement already satisfied: numpy>=1.10.4 in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from gym<0.16.0,>=0.15.4->baselines==0.1.6) (1.22.2)
	Requirement already satisfied: six in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from gym<0.16.0,>=0.15.4->baselines==0.1.6) (1.15.0)
	Collecting pyglet<=1.5.0,>=1.4.0
	  Downloading pyglet-1.5.0-py2.py3-none-any.whl (1.0 MB)
	     ---------------------------------------- 1.0/1.0 MB 13.0 MB/s eta 0:00:00
	Collecting cloudpickle
	  Downloading cloudpickle-1.2.2-py2.py3-none-any.whl (25 kB)
	Requirement already satisfied: colorama in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from click->baselines==0.1.6) (0.4.4)
	Requirement already satisfied: future in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from pyglet<=1.5.0,>=1.4.0->gym<0.16.0,>=0.15.4->baselines==0.1.6) (0.18.2)
	Building wheels for collected packages: baselines, gym
	  Building wheel for baselines (setup.py) ... done
	  Created wheel for baselines: filename=baselines-0.1.6-py3-none-any.whl size=222451 sha256=dcf5fc6144e932bdf4bbc1230a563dbdfbf543e47eb50f00fed75e78ed85a8c2
	  Stored in directory: C:\Users\metol\AppData\Local\Temp\pip-ephem-wheel-cache-r2unacid\wheels\95\45\e7\dcd08d5c5c44be55d57f1d5d71c63bbeab6318fae0d974e8ed
	  Building wheel for gym (setup.py) ... done
	  Created wheel for gym: filename=gym-0.15.7-py3-none-any.whl size=1648842 sha256=68fdfca401253d345b8a48070ce276d41ef79c95ae6df71172b282fffeaf5761
	  Stored in directory: c:\users\metol\appdata\local\pip\cache\wheels\42\c9\4b\5043e144d4319a7ebe7d59be1ad561ed129edecfa73300f096
	Successfully built baselines gym
	Installing collected packages: cloudpickle, tqdm, pyglet, opencv-python, click, gym, baselines
	  Attempting uninstall: cloudpickle
	    Found existing installation: cloudpickle 2.2.0
	    Uninstalling cloudpickle-2.2.0:
	      Successfully uninstalled cloudpickle-2.2.0
	  Attempting uninstall: pyglet
	    Found existing installation: pyglet 1.5.16
	    Uninstalling pyglet-1.5.16:
	      Successfully uninstalled pyglet-1.5.16
	  Attempting uninstall: gym
	    Found existing installation: gym 0.21.0
	    Uninstalling gym-0.21.0:
	ERROR: Could not install packages due to an OSError: [WinError 32] The process cannot access the file because it is being used by another process: 'c:\\users\\metol\\.conda\\envs\\tf_gpu_mygames\\lib\\site-packages\\gym\\'
	Consider using the `--user` option or check the permissions.
 ```

### 2.- Creating Package
```
	tf_gpu_mygames) PS C:\git\learning_AI_games\gym> pip install -e gym-examples
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	Obtaining file:///C:/git/learning_AI_games/gym/gym-examples
	Preparing metadata (setup.py) ... done
	ERROR: More than one .egg-info directory found in C:\Users\metol\AppData\Local\Temp\pip-pip-egg-info-9gsh6mp_
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	(tf_gpu_mygames) PS C:\git\learning_AI_games\gym> pip install -e gym-examples
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	Obtaining file:///C:/git/learning_AI_games/gym/gym-examples
	Preparing metadata (setup.py) ... done
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	Requirement already satisfied: gym==0.21.0 in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from myenv==0.0.1) (0.21.0)
	Collecting numpy==1.19.5
	Using cached numpy-1.19.5-cp39-cp39-win_amd64.whl (13.3 MB)
	Requirement already satisfied: cloudpickle>=1.2.0 in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from
	gym==0.21.0->myenv==0.0.1) (2.2.0)
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	Installing collected packages: numpy, myenv
	Attempting uninstall: numpy
		WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
		Found existing installation: numpy 1.22.2
		Uninstalling numpy-1.22.2:
		Successfully uninstalled numpy-1.22.2
	Running setup.py develop for myenv
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
	tf-nightly-gpu 2.6.0.dev20210327 requires typing-extensions~=3.7.4, but you have typing-extensions 4.0.0 which is incompatible.
	Successfully installed myenv-0.0.1 numpy-1.19.5
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
```

### 3.- Error with packages while installing MyEnv-v0 package
setup file had the following:
```
setup(
    name="myenv",
    version="0.0.1",
    install_requires=["gym==0.21.0", "numpy==1.19.5"]
	)
```
This is all the terminal of my work today:
```
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Try the new cross-platform PowerShell https://aka.ms/pscore6

Loading personal and system profiles took 526ms.
(base) PS C:\git> conda activate tf_gpu_mygames
(tf_gpu_mygames) PS C:\git>  & 'C:\Users\metol\.conda\envs\tf_gpu_mygames\python.exe' 'c:\Users\metol\.vscode\extensions\ms-pytite-packages\gym\envs\classic_control\myenv.py'
	Clay Pit upgraded to level 2!
	Turn 0 - Points: 2899
	Turn 1 - Points: 2638
	Turn 2 - Points: 2377
	Turn 3 - Points: 1815
	Clay Pit upgraded to level 3!
	Turn 4 - Points: 1253
	Turn 5 - Points: 1293
	Turn 6 - Points: 1333
	Turn 7 - Points: 1373
	Woodcutter upgraded to level 2!
	Turn 8 - Points: 1112
	Turn 9 - Points: 1152
(tf_gpu_mygames) PS C:\git>  C:; cd 'C:\git'; & 'C:\Users\metol\.conda\envs\tf_gpu_mygames\python.exe' 'c:\Users\metol\.vscode\extensions\ms-python.python-2022.20.1\pythonFiles\lib\python\debugpy\adapter/../..\debugpy\launcher' '50193' '--' 'c:\git\learning_AI_games\gym\gym-examples\.env\Lib\site-packages\gym\envs\classic_control\myenv.py'
	Crop upgraded to level 2!
	Traceback (most recent call last):
	File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\utils\env_checker.py", line 183, in _check_returned_values
		_check_obs(obs[key], observation_space.spaces[key], "reset")
	File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\utils\env_checker.py", line 83, in _check_obs
		assert isinstance(
	AssertionError: The observation returned by `reset()` method must be an int

	During handling of the above exception, another exception occurred:

	Traceback (most recent call last):
	File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\runpy.py", line 197, in _run_module_as_main
		return _run_code(code, main_globals, None,
	File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\runpy.py", line 87, in _run_code
		exec(code, run_globals)
	File "c:\Users\metol\.vscode\extensions\ms-python.python-2022.20.1\pythonFiles\lib\python\debugpy\__main__.py", line 39, in <module>
		cli.main()
	File "c:\Users\metol\.vscode\extensions\ms-python.python-2022.20.1\pythonFiles\lib\python\debugpy/..\debugpy\server\cli.py",
	line 430, in main
		run()
	File "c:\Users\metol\.vscode\extensions\ms-python.python-2022.20.1\pythonFiles\lib\python\debugpy/..\debugpy\server\cli.py",
	line 284, in run_file
		runpy.run_path(target, run_name="__main__")
	File "c:\Users\metol\.vscode\extensions\ms-python.python-2022.20.1\pythonFiles\lib\python\debugpy\_vendored\pydevd\_pydevd_bundle\pydevd_runpy.py", line 321, in run_path
	File "c:\Users\metol\.vscode\extensions\ms-python.python-2022.20.1\pythonFiles\lib\python\debugpy\_vendored\pydevd\_pydevd_bu    _run_code(code, mod_globals, init_globals,
	ydevd_bundle\pydevd_runpy.py", line 124, in _run_code                                                                  ydevd_bu
		exec(code, run_globals)
	File "c:\git\learning_AI_games\gym\gym-examples\.env\Lib\site-packages\gym\envs\classic_control\myenv.py", line 317,
		check_env(env)                                                                                                     in <modu
	File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\utils\env_checker.py", line 330, in check_env
		_check_returned_values(env, observation_space, action_space)
	File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\utils\env_checker.py", line 185, in _check_returned_values
		raise AssertionError(f"Error while checking key={key}: " + str(e))                                                 rned_val
	AssertionError: Error while checking key=clay_level: The observation returned by `reset()` method must be an int
(tf_gpu_mygames) PS C:\git> conda list
# packages in environment at C:\Users\metol\.conda\envs\tf_gpu_mygames:
#
# Name                    Version                   Build  Channel
absl-py                   0.12.0                   pypi_0    pypi
astroid                   2.8.5            py39hcbf5309_0    conda-forge
astunparse                1.6.3                    pypi_0    pypi
backcall                  0.2.0              pyh9f0ad1d_0    conda-forge
backports                 1.0                        py_2    conda-forge
backports.functools_lru_cache 1.6.4              pyhd8ed1ab_0    conda-forge
ca-certificates           2022.9.24            h5b45459_0    conda-forge
cachetools                4.2.1                    pypi_0    pypi
certifi                   2022.9.24          pyhd8ed1ab_0    conda-forge
chardet                   4.0.0                    pypi_0    pypi
click                     8.1.3                    pypi_0    pypi
cloudpickle               1.2.2                    pypi_0    pypi
colorama                  0.4.4              pyh9f0ad1d_0    conda-forge
cycler                    0.10.0                     py_2    conda-forge
debugpy                   1.5.1            py39h415ef7b_0    conda-forge
decorator                 5.1.1              pyhd8ed1ab_0    conda-forge
entrypoints               0.3             pyhd8ed1ab_1003    conda-forge
ffmpeg                    4.3.1                ha925a31_0    conda-forge
flatbuffers               1.12                     pypi_0    pypi
freetype                  2.10.4               h546665d_1    conda-forge
future                    0.18.2           py39hcbf5309_4    conda-forge
gast                      0.4.0                    pypi_0    pypi
google-auth               1.30.0                   pypi_0    pypi
google-auth-oauthlib      0.4.4                    pypi_0    pypi
google-pasta              0.2.0                    pypi_0    pypi
grpcio                    1.34.1                   pypi_0    pypi
gym                       0.21.0                   pypi_0    pypi
h5py                      3.1.0                    pypi_0    pypi
icu                       68.1                 h0e60522_0    conda-forge
idna                      2.10                     pypi_0    pypi
intel-openmp              2021.2.0           h57928b3_616    conda-forge
ipykernel                 6.6.1            py39h832f523_0    conda-forge
ipython                   7.31.0           py39hcbf5309_0    conda-forge
isort                     5.10.1             pyhd8ed1ab_0    conda-forge
jedi                      0.18.1           py39hcbf5309_0    conda-forge
joblib                    0.17.0                     py_0    anaconda
jpeg                      9d                   h8ffe710_0    conda-forge
jupyter_client            7.1.0              pyhd8ed1ab_0    conda-forge
jupyter_core              4.9.1            py39hcbf5309_1    conda-forge
keras-nightly             2.5.0.dev2021032900          pypi_0    pypi
keras-preprocessing       1.1.2                    pypi_0    pypi
keras-visualizer          2.4                      pypi_0    pypi
kiwisolver                1.3.1            py39h2e07f2f_1    conda-forge
lazy-object-proxy         1.6.0            py39hb82d6ee_1    conda-forge
lcms2                     2.12                 h2a16943_0    conda-forge
libblas                   3.9.0                     8_mkl    conda-forge
libcblas                  3.9.0                     8_mkl    conda-forge
libclang                  11.1.0          default_h5c34c98_0    conda-forge
liblapack                 3.9.0                     8_mkl    conda-forge
libpng                    1.6.37               h1d00b33_2    conda-forge
libsodium                 1.0.18               h8d14728_1    conda-forge
libtiff                   4.2.0                hc10be44_1    conda-forge
lz4-c                     1.9.3                h8ffe710_0    conda-forge
m2w64-gcc-libgfortran     5.3.0                         6    conda-forge
m2w64-gcc-libs            5.3.0                         7    conda-forge
m2w64-gcc-libs-core       5.3.0                         7    conda-forge
m2w64-gmp                 6.1.0                         2    conda-forge
m2w64-libwinpthread-git   5.0.0.4634.697f757               2    conda-forge
markdown                  3.3.4                    pypi_0    pypi
matplotlib                3.4.1            py39hcbf5309_0    conda-forge
matplotlib-base           3.4.1            py39h581301d_0    conda-forge
matplotlib-inline         0.1.3              pyhd8ed1ab_0    conda-forge
mccabe                    0.6.1                      py_1    conda-forge
mkl                       2020.4             hb70f87d_311    conda-forge
msys2-conda-epoch         20160418                      1    conda-forge
nest-asyncio              1.5.4              pyhd8ed1ab_0    conda-forge
numpy                     1.19.5                   pypi_0    pypi
oauthlib                  3.1.0                    pypi_0    pypi
olefile                   0.46               pyh9f0ad1d_1    conda-forge
opencv-python             4.6.0.66                 pypi_0    pypi
openjpeg                  2.4.0                h48faf41_0    conda-forge
openssl                   1.1.1l               h8ffe710_0    conda-forge
opt-einsum                3.3.0                    pypi_0    pypi
pandas                    1.2.4            py39h2e25243_0    conda-forge
parso                     0.8.3              pyhd8ed1ab_0    conda-forge
pickleshare               0.7.5                   py_1003    conda-forge
pillow                    8.1.2            py39h1a9d4f7_1    conda-forge
pip                       22.0.3             pyhd8ed1ab_0    conda-forge
platformdirs              2.3.0              pyhd8ed1ab_0    conda-forge
prompt-toolkit            3.0.24             pyha770c72_0    conda-forge
protobuf                  3.15.8                   pypi_0    pypi
pyasn1                    0.4.8                    pypi_0    pypi
pyasn1-modules            0.2.8                    pypi_0    pypi
pygame                    2.1.2                    pypi_0    pypi
pyglet                    1.5.0                    pypi_0    pypi
pygments                  2.11.2             pyhd8ed1ab_0    conda-forge
pylint                    2.11.1             pyhd8ed1ab_0    conda-forge
pyparsing                 2.4.7              pyh9f0ad1d_0    conda-forge
pyqt                      5.12.3           py39hcbf5309_7    conda-forge
pyqt-impl                 5.12.3           py39h415ef7b_7    conda-forge
pyqt5-sip                 4.19.18          py39h415ef7b_7    conda-forge
pyqtchart                 5.12             py39h415ef7b_7    conda-forge
pyqtwebengine             5.12.1           py39h415ef7b_7    conda-forge
python                    3.9.2           h7840368_0_cpython    conda-forge
python-dateutil           2.8.1                      py_0    conda-forge
python_abi                3.9                      1_cp39    conda-forge
pytz                      2020.1                     py_0    anaconda
pywin32                   303              py39hb82d6ee_0    conda-forge
pyyaml                    6.0              py39hb82d6ee_3    conda-forge
pyzmq                     22.3.0           py39he46f08e_1    conda-forge
qt                        5.12.9               h5909a2a_4    conda-forge
requests                  2.25.1                   pypi_0    pypi
requests-oauthlib         1.3.0                    pypi_0    pypi
rsa                       4.7.2                    pypi_0    pypi
scikit-learn              0.24.2           py39he931e04_0    conda-forge
scipy                     1.6.3            py39hc0c34ad_0    conda-forge
setuptools                49.6.0           py39hcbf5309_3    conda-forge
six                       1.15.0             pyh9f0ad1d_0    conda-forge
sqlite                    3.35.5               h8ffe710_0    conda-forge
tb-nightly                2.5.0a20210419           pypi_0    pypi
tensorboard-data-server   0.6.0                    pypi_0    pypi
tensorboard-plugin-wit    1.8.0                    pypi_0    pypi
termcolor                 1.1.0                    pypi_0    pypi
tf-estimator-nightly      2.5.0.dev2021032601          pypi_0    pypi
tf-nightly-gpu            2.6.0.dev20210327          pypi_0    pypi
threadpoolctl             2.1.0              pyh5ca1d4c_0    anaconda
tk                        8.6.10               h8ffe710_1    conda-forge
toml                      0.10.2             pyhd8ed1ab_0    conda-forge
tornado                   6.1              py39hb82d6ee_1    conda-forge
tqdm                      4.64.1                   pypi_0    pypi
traitlets                 5.1.1              pyhd8ed1ab_0    conda-forge
typing_extensions         4.0.0              pyha770c72_0    conda-forge
urllib3                   1.26.4                   pypi_0    pypi
vc                        14.2                 hb210afc_4    conda-forge
vs2015_runtime            14.28.29325          h5e1d092_4    conda-forge
wcwidth                   0.2.5              pyh9f0ad1d_2    conda-forge
werkzeug                  1.0.1                    pypi_0    pypi
wheel                     0.36.2             pyhd3deb0d_0    conda-forge
xz                        5.2.5                h62dcd97_1    conda-forge
yaml                      0.2.5                h8ffe710_2    conda-forge
zeromq                    4.3.4                h0e60522_1    conda-forge
zlib                      1.2.11            h62dcd97_1010    conda-forge
zstd                      1.4.9                h6255e5f_0    conda-forge
(tf_gpu_mygames) PS C:\git>  C:; cd 'C:\git'; & 'C:\Users\metol\.conda\envs\tf_gpu_mygames\python.exe' 'c:\Users\metol\.vscode\extensions\ms-python.python-2022.20.1\pythonFiles\lib\python\debugpy\adapter/../..\debugpy\launcher' '50335' '-   or: setup.py --help [cmd1 cmd2 ...]
   or: setup.py --help-commands
   or: setup.py cmd --help

error: no commands supplied
(tf_gpu_mygames) PS C:\git> cd .\learning_AI_games\gym\gym-examples\
(tf_gpu_mygames) PS C:\git\learning_AI_games\gym\gym-examples> pip install -e myenv
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
 with bzr+http, bzr+https, bzr+ssh, bzr+sftp, bzr+ftp, bzr+lp, bzr+file, git+http, git+https, git+ssh, git+git, git+file, hg+file, hg+http, hg+https, hg+ssh, hg+static-http, svn+ssh, svn+http, svn+https, svn+svn, svn+file).
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
(tf_gpu_mygames) PS C:\git\learning_AI_games\gym\gym-examples> cd ..
(tf_gpu_mygames) PS C:\git\learning_AI_games\gym> pip install -e gym-examples
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
Obtaining file:///C:/git/learning_AI_games/gym/gym-examples
  Preparing metadata (setup.py) ... done
ERROR: More than one .egg-info directory found in C:\Users\metol\AppData\Local\Temp\pip-pip-egg-info-9gsh6mp_
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
(tf_gpu_mygames) PS C:\git\learning_AI_games\gym> pip install -e gym-examples
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
Obtaining file:///C:/git/learning_AI_games/gym/gym-examples
  Preparing metadata (setup.py) ... done
  WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
Requirement already satisfied: gym==0.21.0 in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from myenv==0.0.1) (0.21.0)
Collecting numpy==1.19.5
  Using cached numpy-1.19.5-cp39-cp39-win_amd64.whl (13.3 MB)
Requirement already satisfied: cloudpickle>=1.2.0 in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from
gym==0.21.0->myenv==0.0.1) (2.2.0)
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
Installing collected packages: numpy, myenv
  Attempting uninstall: numpy
    Found existing installation: numpy 1.22.2
    Uninstalling numpy-1.22.2:
      Successfully uninstalled numpy-1.22.2
  Running setup.py develop for myenv
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
tf-nightly-gpu 2.6.0.dev20210327 requires typing-extensions~=3.7.4, but you have typing-extensions 4.0.0 which is incompatible.
Successfully installed myenv-0.0.1 numpy-1.19.5
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
(tf_gpu_mygames) PS C:\git\learning_AI_games\gym> python
Python 3.9.2 | packaged by conda-forge | (default, Feb 21 2021, 04:59:43) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import gym_examples
>>> env = gym.make('classic_control/MyEnv-v0')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'gym' is not defined
>>> import gym
>>> env = gym.make('classic_control/MyEnv-v0')
Traceback (most recent call last):
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 158, in spec
    return self.env_specs[id]
KeyError: 'classic_control/MyEnv-v0'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 235, in make
    return registry.make(id, **kwargs)
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 128, in make
    spec = self.spec(path)
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 203, in spec
    raise error.UnregisteredEnv("No registered env with id: {}".format(id))
gym.error.UnregisteredEnv: No registered env with id: classic_control/MyEnv-v0
>>> env = gym.make('classic_control/BipedalWalker-v3')
Traceback (most recent call last):
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 158, in spec
    return self.env_specs[id]
KeyError: 'classic_control/BipedalWalker-v3'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 235, in make
    return registry.make(id, **kwargs)
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 128, in make
    spec = self.spec(path)
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 185, in spec
    raise error.DeprecatedEnv(
gym.error.DeprecatedEnv: Env classic_control/BipedalWalker-v3 not found (valid versions include ['BipedalWalker-v3'])
>>> env = gym.make('classic_control/BipedalWalker-v3')
Traceback (most recent call last):
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 158, in spec
    return self.env_specs[id]
KeyError: 'classic_control/BipedalWalker-v3'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 235, in make
    return registry.make(id, **kwargs)
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 128, in make
    spec = self.spec(path)
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 185, in spec
    raise error.DeprecatedEnv(
gym.error.DeprecatedEnv: Env classic_control/BipedalWalker-v3 not found (valid versions include ['BipedalWalker-v3'])
>>> env = gym.make('BipedalWalker-v3')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 235, in make
    return registry.make(id, **kwargs)
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 129, in make
    env = spec.make(**kwargs)
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 89, in make
    cls = load(self.entry_point)
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 28, in load
    fn = getattr(mod, attr_name)
AttributeError: module 'gym.envs.box2d' has no attribute 'BipedalWalker'
>>> env = gym.make('MyEnv-v0')
Traceback (most recent call last):
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 158, in spec
    return self.env_specs[id]
KeyError: 'MyEnv-v0'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 235, in make
    return registry.make(id, **kwargs)
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 128, in make
    spec = self.spec(path)
    raise error.UnregisteredEnv("No registered env with id: {}".format(id))
gym.error.UnregisteredEnv: No registered env with id: MyEnv-v0
>>> env = gym.make("LunarLander-v2", render_mode="human")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 235, in make
    return registry.make(id, **kwargs)
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 129, in make
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 89, in make
    cls = load(self.entry_point)
  File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 28, in load
    fn = getattr(mod, attr_name)
AttributeError: module 'gym.envs.box2d' has no attribute 'LunarLander'
>>> exit()
(tf_gpu_mygames) PS C:\git\learning_AI_games\gym> import gym
import : The term 'import' is not recognized as the name of a cmdlet, function, script file, or operable program.
Check the spelling of the name, or if a path was included, verify that the path is correct and try again.
At line:1 char:1
+ import gym
+ ~~~~~~
    + CategoryInfo          : ObjectNotFound: (import:String) [], CommandNotFoundException
    + FullyQualifiedErrorId : CommandNotFoundException

(tf_gpu_mygames) PS C:\git\learning_AI_games\gym> python
	Python 3.9.2 | packaged by conda-forge | (default, Feb 21 2021, 04:59:43) [MSC v.1916 64 bit (AMD64)] on win32
	Type "help", "copyright", "credits" or "license" for more information.
	>>> import gym
	>>> env = gym.make('CartPole-v0')
	>>> env = gym.make('CartPole-v1')
	>>> env = gym.make('AcrobotEnv-v1')
	Traceback (most recent call last):
	File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 158, in spec
		return self.env_specs[id]
	KeyError: 'AcrobotEnv-v1'

	During handling of the above exception, another exception occurred:

	Traceback (most recent call last):
	File "<stdin>", line 1, in <module>
	File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 235, in make
		return registry.make(id, **kwargs)
	File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 128, in make
		spec = self.spec(path)
		raise error.UnregisteredEnv("No registered env with id: {}".format(id))
	gym.error.UnregisteredEnv: No registered env with id: AcrobotEnv-v1
	>>> env = gym.make('LunarLanderContinuous-v2')
	Traceback (most recent call last):
	File "<stdin>", line 1, in <module>
	File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 235, in make
		return registry.make(id, **kwargs)
	File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 129, in make
		env = spec.make(**kwargs)
	File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 89, in make
		cls = load(self.entry_point)
	File "C:\Users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages\gym\envs\registration.py", line 28, in load
		fn = getattr(mod, attr_name)
	AttributeError: module 'gym.envs.box2d' has no attribute 'LunarLanderContinuous'
	>>> exit()
(tf_gpu_mygames) PS C:\git\learning_AI_games\gym> conda list

CondaError: Expected exactly one `egg-info` directory in 'C:\git\learning_AI_games\gym\gym-examples', via egg-link 'Lib/site-packages/myenv.egg-link'. Instead found: ('gym_examples.egg-info', 'myenv.egg-info').  These are often left over
from legacy operations that did not clean up correctly.  Please remove all but one of these.

(tf_gpu_mygames) PS C:\git\learning_AI_games\gym>

```
I deleted 'myenv.egg-info'. Here are conda and pip outputs
```
(tf_gpu_mygames) PS C:\git\learning_AI_games\gym> conda list
	# packages in environment at C:\Users\metol\.conda\envs\tf_gpu_mygames:
	#
	# Name                    Version                   Build  Channel
	absl-py                   0.12.0                   pypi_0    pypi
	astroid                   2.8.5            py39hcbf5309_0    conda-forge
	astunparse                1.6.3                    pypi_0    pypi
	backcall                  0.2.0              pyh9f0ad1d_0    conda-forge
	backports                 1.0                        py_2    conda-forge
	backports.functools_lru_cache 1.6.4              pyhd8ed1ab_0    conda-forge
	ca-certificates           2022.9.24            h5b45459_0    conda-forge
	cachetools                4.2.1                    pypi_0    pypi
	certifi                   2022.9.24          pyhd8ed1ab_0    conda-forge
	chardet                   4.0.0                    pypi_0    pypi
	click                     8.1.3                    pypi_0    pypi
	cloudpickle               1.2.2                    pypi_0    pypi
	colorama                  0.4.4              pyh9f0ad1d_0    conda-forge
	cycler                    0.10.0                     py_2    conda-forge
	debugpy                   1.5.1            py39h415ef7b_0    conda-forge
	decorator                 5.1.1              pyhd8ed1ab_0    conda-forge
	entrypoints               0.3             pyhd8ed1ab_1003    conda-forge
	ffmpeg                    4.3.1                ha925a31_0    conda-forge
	flatbuffers               1.12                     pypi_0    pypi
	freetype                  2.10.4               h546665d_1    conda-forge
	future                    0.18.2           py39hcbf5309_4    conda-forge
	gast                      0.4.0                    pypi_0    pypi
	google-auth               1.30.0                   pypi_0    pypi
	google-auth-oauthlib      0.4.4                    pypi_0    pypi
	google-pasta              0.2.0                    pypi_0    pypi
	grpcio                    1.34.1                   pypi_0    pypi
	gym                       0.21.0                   pypi_0    pypi
	gym-examples              0.0.1                     dev_0    <develop>
	h5py                      3.1.0                    pypi_0    pypi
	icu                       68.1                 h0e60522_0    conda-forge
	idna                      2.10                     pypi_0    pypi
	intel-openmp              2021.2.0           h57928b3_616    conda-forge
	ipykernel                 6.6.1            py39h832f523_0    conda-forge
	ipython                   7.31.0           py39hcbf5309_0    conda-forge
	isort                     5.10.1             pyhd8ed1ab_0    conda-forge
	jedi                      0.18.1           py39hcbf5309_0    conda-forge
	joblib                    0.17.0                     py_0    anaconda
	jpeg                      9d                   h8ffe710_0    conda-forge
	jupyter_client            7.1.0              pyhd8ed1ab_0    conda-forge
	jupyter_core              4.9.1            py39hcbf5309_1    conda-forge
	keras-nightly             2.5.0.dev2021032900          pypi_0    pypi
	keras-preprocessing       1.1.2                    pypi_0    pypi
	keras-visualizer          2.4                      pypi_0    pypi
	kiwisolver                1.3.1            py39h2e07f2f_1    conda-forge
	lazy-object-proxy         1.6.0            py39hb82d6ee_1    conda-forge
	lcms2                     2.12                 h2a16943_0    conda-forge
	libblas                   3.9.0                     8_mkl    conda-forge
	libcblas                  3.9.0                     8_mkl    conda-forge
	libclang                  11.1.0          default_h5c34c98_0    conda-forge
	liblapack                 3.9.0                     8_mkl    conda-forge
	libpng                    1.6.37               h1d00b33_2    conda-forge
	libsodium                 1.0.18               h8d14728_1    conda-forge
	libtiff                   4.2.0                hc10be44_1    conda-forge
	lz4-c                     1.9.3                h8ffe710_0    conda-forge
	m2w64-gcc-libgfortran     5.3.0                         6    conda-forge
	m2w64-gcc-libs            5.3.0                         7    conda-forge
	m2w64-gcc-libs-core       5.3.0                         7    conda-forge
	m2w64-gmp                 6.1.0                         2    conda-forge
	m2w64-libwinpthread-git   5.0.0.4634.697f757               2    conda-forge
	markdown                  3.3.4                    pypi_0    pypi
	matplotlib                3.4.1            py39hcbf5309_0    conda-forge
	matplotlib-base           3.4.1            py39h581301d_0    conda-forge
	matplotlib-inline         0.1.3              pyhd8ed1ab_0    conda-forge
	mccabe                    0.6.1                      py_1    conda-forge
	mkl                       2020.4             hb70f87d_311    conda-forge
	msys2-conda-epoch         20160418                      1    conda-forge
	nest-asyncio              1.5.4              pyhd8ed1ab_0    conda-forge
	numpy                     1.19.5                   pypi_0    pypi
	oauthlib                  3.1.0                    pypi_0    pypi
	olefile                   0.46               pyh9f0ad1d_1    conda-forge
	opencv-python             4.6.0.66                 pypi_0    pypi
	openjpeg                  2.4.0                h48faf41_0    conda-forge
	openssl                   1.1.1l               h8ffe710_0    conda-forge
	opt-einsum                3.3.0                    pypi_0    pypi
	pandas                    1.2.4            py39h2e25243_0    conda-forge
	parso                     0.8.3              pyhd8ed1ab_0    conda-forge
	pickleshare               0.7.5                   py_1003    conda-forge
	pillow                    8.1.2            py39h1a9d4f7_1    conda-forge
	pip                       22.0.3             pyhd8ed1ab_0    conda-forge
	platformdirs              2.3.0              pyhd8ed1ab_0    conda-forge
	prompt-toolkit            3.0.24             pyha770c72_0    conda-forge
	protobuf                  3.15.8                   pypi_0    pypi
	pyasn1                    0.4.8                    pypi_0    pypi
	pyasn1-modules            0.2.8                    pypi_0    pypi
	pygame                    2.1.2                    pypi_0    pypi
	pyglet                    1.5.0                    pypi_0    pypi
	pygments                  2.11.2             pyhd8ed1ab_0    conda-forge
	pylint                    2.11.1             pyhd8ed1ab_0    conda-forge
	pyparsing                 2.4.7              pyh9f0ad1d_0    conda-forge
	pyqt                      5.12.3           py39hcbf5309_7    conda-forge
	pyqt-impl                 5.12.3           py39h415ef7b_7    conda-forge
	pyqt5-sip                 4.19.18          py39h415ef7b_7    conda-forge
	pyqtchart                 5.12             py39h415ef7b_7    conda-forge
	pyqtwebengine             5.12.1           py39h415ef7b_7    conda-forge
	python                    3.9.2           h7840368_0_cpython    conda-forge
	python-dateutil           2.8.1                      py_0    conda-forge
	python_abi                3.9                      1_cp39    conda-forge
	pytz                      2020.1                     py_0    anaconda
	pywin32                   303              py39hb82d6ee_0    conda-forge
	pyyaml                    6.0              py39hb82d6ee_3    conda-forge
	pyzmq                     22.3.0           py39he46f08e_1    conda-forge
	qt                        5.12.9               h5909a2a_4    conda-forge
	requests                  2.25.1                   pypi_0    pypi
	requests-oauthlib         1.3.0                    pypi_0    pypi
	rsa                       4.7.2                    pypi_0    pypi
	scikit-learn              0.24.2           py39he931e04_0    conda-forge
	scipy                     1.6.3            py39hc0c34ad_0    conda-forge
	setuptools                49.6.0           py39hcbf5309_3    conda-forge
	sqlite                    3.35.5               h8ffe710_0    conda-forge
	tb-nightly                2.5.0a20210419           pypi_0    pypi
	tensorboard-data-server   0.6.0                    pypi_0    pypi
	tensorboard-plugin-wit    1.8.0                    pypi_0    pypi
	termcolor                 1.1.0                    pypi_0    pypi
	tf-estimator-nightly      2.5.0.dev2021032601          pypi_0    pypi
	tf-nightly-gpu            2.6.0.dev20210327          pypi_0    pypi
	threadpoolctl             2.1.0              pyh5ca1d4c_0    anaconda
	tk                        8.6.10               h8ffe710_1    conda-forge
	toml                      0.10.2             pyhd8ed1ab_0    conda-forge
	tornado                   6.1              py39hb82d6ee_1    conda-forge
	tqdm                      4.64.1                   pypi_0    pypi
	traitlets                 5.1.1              pyhd8ed1ab_0    conda-forge
	typing-extensions         3.7.4.3                  pypi_0    pypi
	typing_extensions         4.0.0              pyha770c72_0    conda-forge
	tzdata                    2021a                he74cb21_0    conda-forge
	urllib3                   1.26.4                   pypi_0    pypi
	vc                        14.2                 hb210afc_4    conda-forge
	vs2015_runtime            14.28.29325          h5e1d092_4    conda-forge
	wcwidth                   0.2.5              pyh9f0ad1d_2    conda-forge
	werkzeug                  1.0.1                    pypi_0    pypi
	wheel                     0.36.2             pyhd3deb0d_0    conda-forge
	wincertstore              0.2             py39hcbf5309_1006    conda-forge
	wrapt                     1.12.1           py39hb82d6ee_3    conda-forge
	xz                        5.2.5                h62dcd97_1    conda-forge
	yaml                      0.2.5                h8ffe710_2    conda-forge
	zeromq                    4.3.4                h0e60522_1    conda-forge
	zlib                      1.2.11            h62dcd97_1010    conda-forge
	zstd                      1.4.9                h6255e5f_0    conda-forge
(tf_gpu_mygames) PS C:\git\learning_AI_games\gym> pip list
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	Package                       Version
	----------------------------- -------------------
	absl-py                       0.12.0
	astroid                       2.8.5
	astunparse                    1.6.3
	backcall                      0.2.0
	backports.functools-lru-cache 1.6.4
	cachetools                    4.2.1
	certifi                       2022.9.24
	chardet                       4.0.0
	click                         8.1.3
	cloudpickle                   2.2.0
	colorama                      0.4.4
	cycler                        0.10.0
	debugpy                       1.5.1
	decorator                     5.1.1
	entrypoints                   0.3
	flatbuffers                   1.12
	future                        0.18.2
	gast                          0.4.0
	google-auth                   1.30.0
	google-auth-oauthlib          0.4.4
	google-pasta                  0.2.0
	grpcio                        1.34.1
	gym                           0.21.0
	gym-examples                  0.0.1
	h5py                          3.1.0
	idna                          2.10
	ipykernel                     6.6.1
	ipython                       7.31.0
	isort                         5.10.1
	jedi                          0.18.1
	joblib                        0.17.0
	jupyter-client                7.1.0
	jupyter-core                  4.9.1
	keras-nightly                 2.5.0.dev2021032900
	Keras-Preprocessing           1.1.2
	keras-visualizer              2.4
	kiwisolver                    1.3.1
	lazy-object-proxy             1.6.0
	Markdown                      3.3.4
	matplotlib                    3.4.1
	matplotlib-inline             0.1.3
	mccabe                        0.6.1
	nest-asyncio                  1.5.4
	numpy                         1.19.5
	oauthlib                      3.1.0
	olefile                       0.46
	opencv-python                 4.6.0.66
	opt-einsum                    3.3.0
	pandas                        1.2.4
	parso                         0.8.3
	pickleshare                   0.7.5
	Pillow                        8.1.2
	pip                           22.0.3
	platformdirs                  2.3.0
	prompt-toolkit                3.0.24
	protobuf                      3.15.8
	pyasn1                        0.4.8
	pyasn1-modules                0.2.8
	pygame                        2.1.2
	pyglet                        1.5.0
	Pygments                      2.11.2
	pylint                        2.11.1
	pyparsing                     2.4.7
	PyQt5                         5.12.3
	PyQt5_sip                     4.19.18
	PyQtChart                     5.12
	PyQtWebEngine                 5.12.1
	python-dateutil               2.8.1
	pytz                          2020.1
	pywin32                       303
	PyYAML                        6.0
	pyzmq                         22.3.0
	requests                      2.25.1
	requests-oauthlib             1.3.0
	rsa                           4.7.2
	scikit-learn                  0.24.2
	scipy                         1.6.3
	setuptools                    49.6.0.post20210108
	six                           1.15.0
	tb-nightly                    2.5.0a20210419
	tensorboard-data-server       0.6.0
	tensorboard-plugin-wit        1.8.0
	termcolor                     1.1.0
	tf-estimator-nightly          2.5.0.dev2021032601
	tf-nightly-gpu                2.6.0.dev20210327
	threadpoolctl                 2.1.0
	toml                          0.10.2
	tornado                       6.1
	tqdm                          4.64.1
	traitlets                     5.1.1
	typing_extensions             4.0.0
	urllib3                       1.26.4
	wcwidth                       0.2.5
	Werkzeug                      1.0.1
	wheel                         0.36.2
	wincertstore                  0.2
	wrapt                         1.12.1
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
	WARNING: Ignoring invalid distribution -ym (c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages)
```
