/**
 * Визуальный элемент - список групп - просто список  
 * как раз тут будем делать всякие украшательства списка тумбочек :-)  
 * 
 * (c) A.Golibroda 2019
 * 
 */

import { Component, OnInit } from '@angular/core';

import { Group } from '../_models/group';
import { GroupDataService } from '../_data_services/group-data.service';


import { MAIN_COLOR, COLORS, ColorSelector } from '../_config/colors';



@Component({
  selector: 'app-groups',
  templateUrl: './groups.component.html',
  styleUrls: ['./groups.component.css']
})


export class GroupsComponent implements OnInit {

	groupsList: Group[];
	itemColor: ColorSelector;
	
	constructor(private groupListDataService: GroupDataService) { 
		this.itemColor = new ColorSelector();
	}

	/**
	 * При старте формочки "просмотр списка групп"
	 * 
	 *  Происходят следующие везчи:
	 *  - выбираем первую страницу глобального списка групп. 
	 * 
	 * 
	 */
	ngOnInit(): void {
		
		this.groupListDataService.getAll()
		.subscribe((_groupsList: Group[]) => {
			// вот тут нужно перебрать все элементы списка групп, а в каждую всунуть цвет, который стоит взять из
			// списка цветов, о которых знает система.
			this.groupsList = _groupsList.map((group) => {
				group.color = this.itemColor.get();//'primary';
				return group;
			});
			
			return this.groupsList;
		});
	}

}
