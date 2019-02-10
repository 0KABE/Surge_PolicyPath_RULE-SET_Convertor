# Surge_PolicyPath_RULE-SET_Convertor
将含有Surge3 Pro支持的PolicyPath&amp;RULE-SET转化为普通的配置文件

本脚本使用Python3写成。

由于Clash For Windows并不支持Surge3 Pro中的PolicyPath, RULE-SET规则，所以编写了该脚本来实现将PolicyPath, RULE-SET展开。
目前本人使用的该脚本的方法：

    1、在Surge3 Pro中正确编写配置文件确认无误后，将其导出至PC中，修改脚本文件中的导入以及导出文件地址（建议使用PC iCloud的自动同步）。
    
    2、运行脚本文件（时间可能会有些长，如果需要优化性能的请提交issues，就我自己用就摸鱼了(￣▽￣)"）
    
    3、将导出的配置文件上传至GitHub Gist，至此，可以选择将其转化为Clash For Windows或直接当作Surge3 Pro托管使用。
    
如果使用中发现BUG请提交issues。
