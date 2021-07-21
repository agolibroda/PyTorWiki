/**
 * Всяческие глобальные настройки
 * 
 * import { REST_SERVER_URL, MAIN_MENU } 			from '_config/main'; 
 * 
 */

export const REST_SERVER_URL: string =  'http://localhost:8888';

export const MAIN_SITE_TITLE: string =  'Vedogon';

export const MAIN_MENU = {
		groups: {path: '/groups', title: "Безопасность в ...", icon: "dashboard"}, // Види І Форми Дозвілля
		authors: {path: '/authors', title:"Авторы", icon: "group"},
		newArticle: {path: '/article', title:"Добавить статью", icon: "tab"}, // 'Нова Стаття'
		newGroup: {path: '/group', title:"Добавить раздел", icon: "list_alt"} // Вид Або Форма Дозвілля

		
		
}

