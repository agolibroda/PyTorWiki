# абота с шаблонами
#
#
#
#
#
#
#
#

class TemplateEngier:
    """
    Обработка шаблонов
    
    """
    
    def __init__(self):
        pass
    
    def render(self ):
        pass
    
    
    def temtlatePrepare(self, articleTemplateId): # article_template_id
        """
        Подготовка шаблона - надо пройти по шаблону, и зменить все вызовы вида
         "{% tw_include "main_site_menu" %}" на "{% include ".../tmp/334.html" %}" 
         - с имененм файла, вместо имени шаблона, и, положить все шаблоны в даректорию, где лежат все шаблоны
        Шаблон удаляется из хрнилища при редактировании, кладется  - при первом оращении.
        
        Пока меняем 2 типа операций  
        include =>> tw_include  - включение одного файла - шаблона в другой шаблон
        extends =>> tw_extends - расширение базового шаблона новыми плюшками.  
        
        Все остальное  - оставляем в рамках синтаксиса базового шаблонизатора 
        описание  - https://www.tornadoweb.org/en/stable/template.html
        
        """
        templateEnginer = Template()
        tmlFullName = templateEnginer.realFileName(articleTemplateId)
        logging.info( 'temtlatePrepare:: save 3 tmlFullName =  ' + str(tmlFullName))
        if not templateEnginer.exists(tmlFullName):
#             (template, tlFile) = yield executor.submit( artHelper.getArticleById, article.article_template_id )
            (template, tlFile) = artHelper.getArticleById( articleTemplateId )
            # проанализируем код полученного шаблона, и, если надо, тогда выгрузим все шаблоны, на которые ссылается текущий шаблон.
            #Всевызовы завершим заменами  tw_include на include с соответствующей выгрузкой шаблонов 
            templateEnginer.save(tmlFullName, template.article_source)
        return tmlFullName



    
    