def refine_context(context:str)->str:
    if '最大公因数' in context:
        context = context[:10]
        return context
    elif '整数' in context:
        context = context[len(context)-10:]
        context = context.replace('因数有哪些','')
        return context
    elif '一起吃' in context:
        context = context[:20]
        context = context.replace('一起吃','')
        return context
    elif '氧化' in context and '酸性' in context:
        context = context[:10]
        context = context.replace('反应','')
        return context
    elif '国家' in context and '保险' in context:
        context = context[:10]
        return context
    elif '歌曲：' in context:
        context = context[:10]
        return context
    context = context.replace('_百度知道','')
    context = context.replace('_有问必答_快速问医生','')
    context = context.replace('_39健康问答_39健康网', '')
    context = context.replace('你好', '')
    context = context.replace('1.','')
    context = context.replace('2.','')
    context = context.replace('3.','')
    context = context.replace('一样','')
    context = context.replace('是一个汉语词汇','')
    context = context.replace('拼音', '')
    context = context.replace('笔画', '')
    context = context.replace('病情分析: ','')
    context = context.replace('指导意见: ','')
    return context