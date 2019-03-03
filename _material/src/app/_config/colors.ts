/**
 * Списки цветов, или, цветовые схемы 
 * 
 * (c) A.Golibroda 2019
 * 
 */
//  дадим список правильных цветов, которые может использовать система!!!


//		purple,
//		azure,
//		green, 
//		orange,
//		danger


export const MAIN_COLOR: string =  'danger';

export const COLORS: string[] = 
	[
		'info',
		'success',
		'warning',
		'danger',
		'primary'
	];


interface ListСontainingСolor {
	color: string;
};


/**
 * Класс для перебора цветов из схемы, что бы сделать некие визуальные объекта 
 * зело весёленькими.
 * 
 */
export class ColorSelector {
    curentId: number = 0;
//    constructor(public firstName: string, public middleInitial: string, public lastName: string) {
//        this.fullName = firstName + " " + middleInitial + " " + lastName;
//    }

	get(){
		if (this.curentId >= COLORS.length) {
			this.curentId = 0;
		}
		return COLORS[this.curentId++];
	}
	
//  сделать процедуру загрузки цветов 	
	// для процедуры нужно:
	// сделать интерфейс - "всякие списки, в элементах которых есть слово "цвет"" 
	// этот тип передать в процедуру
	setColors(itemsList: ListСontainingСolor[]){
		return itemsList.map((oneItem) => {
			oneItem.color = this.get();
			return oneItem;
		});
	}
	
}