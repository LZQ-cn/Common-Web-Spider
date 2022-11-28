各个表的信息如下:

default.db:
	位置: 当前目录
	所含表: ini, echo, default_opition

	int 数据信息:
		save_dir : TEXT			--- 爬虫默认文件保存目录
		save_file: TEXT			--- 爬虫默认文件保存名称
		
		header: TEXT			--- 爬虫默认请求头
		ip    : TEXT			--- 爬虫默认 IP
		
		history_path: TEXT		--- 爬取历史默认保存目录

	echo 数据信息:
		change_spider_ini: TEXT	--- 是否提示更改爬虫默认选项

	default_opition 数据信息:
		change_spider_ini: TEXT	--- 当用户在被询问是否修改爬虫配置默认选项时, 用户键入回车的默认选项


