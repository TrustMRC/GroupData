# 技术报告

## 基于 Normalized Levenshtein Distance 的无标签文本聚类

我们首先定义一个文本对 {a,b} 之间的 Normalized Levenshtein Distance为

$$
\text{normalized lev}_{a,b} = \frac{\text{lev}_{a,b}(|a|,|b|)}{|a| + |b|}
$$
在这里$|a|$ 和 $|b|$ 分别表示 $a,b$ 两个字符串的长度， $\text{lev}_{a,b}(|a|,|b|)$ 为 文本对 {a,b} 之间的非归一化 levenshtein 距离, 具体而言
$$
{\displaystyle \qquad \operatorname {lev} _{a,b}(i,j)={\begin{cases}\max(i,j)&{\text{ if }}\min(i,j)=0,\\\min {\begin{cases}\operatorname {lev} _{a,b}(i-1,j)+1\\\operatorname {lev} _{a,b}(i,j-1)+1\\\operatorname {lev} _{a,b}(i-1,j-1)+1_{(a_{i}\neq b_{j})}\end{cases}}&{\text{ otherwise.}}\end{cases}}}
$$
$1_{(a_{i}\neq b_{j})}$是一个**指示函数**（**indicator** **function**），当 ${ a_{i}=b_{j}}$时，其值为0，其他时候它等于 1 。

${ \operatorname {lev} _{a,b}(i,j)}$表示 ${ a}$ 的前i 个字符与 $b$ 的前  $j$  个字符之间的列文斯坦距离。（ $i$ 和 $j$ 都是从1开始的下标)

不难看出，Normalized Levenshtein Distance的取值范围为 (0,1)

据此，我们可以设定，当一个文本对 {a,b} 的 $\text{normalized lev}_{a,b}$ < $\gamma$ 时，我们可以认为 {a,b} 互为一对扰动文本，$\gamma$ 是一个需要调节的超参数，

依次计算，整个数据集中所有文本对之间的距离，当存在一组文本集合 $A$ 且集合中的任意两篇文本组成的文本对的normalized levensthein distance都小于 $\gamma$ 时，我们称这一组文本之间，为一个扰动文本集合，这样我们便完成了文本聚类任务 