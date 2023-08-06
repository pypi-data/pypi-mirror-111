基于sklearn的算法平台
====
1.环境需求
----
        python2.7
        gcc 4.8以上版本
2.环境安装
----
### 安装python2.7

```Bash
#安装依赖(需要切换到root)
cd depends
bash setup.sh
```
3.运行
----
```Bash
cd demo/xiaozhuan
mkdir log result
python __main__.py
# 如果出现缺少依赖的问题，可以安装对应的依赖
```

4.结果查看
----
```Bash
cd demo/xiaozhuan/result/v1
ls -l
```

        ├── box   (箱图)
        ├── cross_predict.txt （交叉验证预测文件）
        ├── cross.txt  （交叉验证效果）
        ├── deleted_feature.txt  （需要删除的特征）
        ├── demo_feature_weight.txt  （特征权重）
        ├── demo.m   （模型）
        ├── feature_with_feature  （特征与特征相似度）
        ├── feature_with_label   （特征与标签相似度）
        ├── hist    （分布图）
        ├── model
        ├── predict_result.txt  （测试集预测结果）
        └── test_score.txt      （测试集上评分）

5.项目启动
----
见doc/start.docx