一款用Python编写的Fuzz工具

目前实现功能：
  基于YAML文件的批量POC验证工具
  基于公司名字的ICP查询并对查询到的网址执行POC批量验证
  基于URL的扫描
	
局限性：
  只能接受YAML文件，且匹配的规则只有method、headers、path、body、expression
  ICP查询没有涉及到基于URL的ICP查询

未来：
  添加子域名爆破、目录扫描、POC批量验证、端口扫描、指纹识别等功能
