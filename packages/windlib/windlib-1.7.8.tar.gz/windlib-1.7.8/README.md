# **Windlib**

有用的函数库，由SNWCreations创建。

这对每个人都是有用的函数库。

## **用法**

### **typeof**

typeof(variate) -> str

检测变量类型，返回字符串。

示例:

    >>> a = 10
    >>> typeof(a)
    'int'

---

### **extract**

extract(filename: str, target_dir: str) -> None

支持“.zip”，“.gz”，“.tar”，“.rar”，“.tar.gz”文件。

如果需要支持rar文件，则需要 "rarfile" 库。

您可以从 https://sourceforge.net/projects/rarfile.berlios/files/latest/download 下载 rarfile 库。

---

### **get_file-从Internet下载文件。**

get_file(url: str, save_path: str) -> str

从 互联网 下载文件，并附带一个进度条。

当下载出错时，会返回'DOWNLOAD_FAILED'。

当下载成功时，目标文件在本地的路径会被返回。

---

### **file_or_dir_exists**

file_or_dir_exists(target: str) -> str

检查指定的文件(或文件夹)是否存在。

当目标是目录时，会返回'IS_DIR'。

当目标是文件时，会返回'IS_FILE'。

当函数找不到目标时，会返回'NOT_FOUND'。

当目标不是有效路径是，会返回'TARGET_INVAILD'。

---

### **find_files_with_the_specified_extension**

find_files_with_the_specified_extension(file_type: str, folder: str, slient: bool) -> list

在目标文件夹中找到具有指定扩展名的文件，返回值是一个列表。

参数 “folder” 的默认值为“.” （当前目录）

“file_type” 变量必须是扩展名，并且不需要带有 “.” 。

例如 "txt", "jar", "md", "class" 或 ".txt" ".jar" ".md" ".class".

---

### **copy_file**

copy_file(src: str or list, dst: str) -> str

复制文件（或文件夹）到指定的目录。

可以通过列表的方式同时将多个文件复制到指定目录。

---

### **is_it_broken**

is_it_broken(path: str or list) -> bool or list

检查一个文件（或目录）是否损坏。

允许调用时通过列表检查大量文件和目录。

若使用列表来检查文件，则返回一个记录所有损坏的文件路径的列表。

示例:

    >>> is_it_broken('./aaa.txt')
    False
    >>> is_it_broken(['./aaa.txt', './bbb.txt', './ccc.txt'])
    []

---

### **pushd**

pushd(new_dir: str)

临时切换到一个目录，操作完成后自动返回调用前路径。

此函数为生成器，请配合 with 语句使用。

示例:

    >>> print(os.getcwd())
    'D:\\windlib-test'
    >>> with pushd('./aaa'):
    ...    print(os.getcwd())
    'D:\\windlib-test\\aaa'
    >>> print(os.getcwd())
    'D:\\windlib-test'

---

### **compress_to_zip_file**

compress_to_zip_file(input_path: str, output_path: str, output_name: str) -> None

压缩一个目录下的所有文件到一个zip文件，无返回值。

示例:

    >>> compress_to_zip_file('./a', '.', 'a.zip')
    >>>

---

### **get_sha1**

get_sha1(path: str) -> str

获取一个文件的SHA1校验值，返回值是一个字符串。

示例:

    >>> get_sha1('setup.py')
    'acdf35508f4dfb49e522f161a3e3e885adbf3b99'

---

### **get_md5**

获取一个文件的MD5校验值，返回值是一个字符串。

示例:

    >>> get_md5('setup.py')
    'ec210fa5cc05bed851da3fe222b733a9'

---

版权所有 (C) 2021 SNWCreations。

欢迎对此库做出 Commit 和 Pull Request!

