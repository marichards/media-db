GrowthDataEditor=function(o) {
    this.init_funcs=[]
    this.urlmap={}
    this.urlmap_url='/defined_media/api/urlmap'
    this.uptake_n=$('.uptake_rm_button').length+1
}


GrowthDataEditor.prototype={
    push_init_func : function(f, args) { 
        this.init_funcs.push([f, args]) 
    },

    init : function() {
	// start off by getting the urlmap, on which other funcs depend
	// since this is an ajax call, the only way to be sure fetching the
	// urlmap has completed is to put the other calls in it's sucess func.
	editor=document.editor
	settings={
	    success: function(data, textStatus, jqXHR) {
	        editor.store_urlmap(data)
		for (i in editor.init_funcs) {
		    init_f=editor.init_funcs[i][0]
		    args=editor.init_funcs[i][1]
		    init_f.apply(undefined, args)
		}
	    },
	    error: function(jqXHR, textStatus, errorThrown) {
		msg='download_urlmap: '+textStatus+'('+errorThrown+')'
		throw msg
	    },
	}
	$.ajax(editor.urlmap_url, settings)
    },

    store_urlmap : function(data) { this.urlmap=data },

    init_callbacks : function() {
	$('#id_growthdata_form').submit(document.editor.prevent_submission)
	$('#id_submit_button').click(document.editor.submit)
	$('#id_add_uptake1').click(document.editor.add_uptake)
    },


    //
    // Add/remove uptake rows:
    //
    add_uptake : function(eventObj) {
	// this is a callback for when an 'Add' button is clicked.
	// It inserts a new uptake row into the document.
	console.log('hi from add_uptake')

	// create tr element and three td elements:
	n=document.editor.uptake_n+1
	console.log('n is '+n)
	row=$('<tr></tr>', {id: 'id_uptake_row'+n})
	row.append($('<td></td>').append($('<input>', {id:'id_uptake_comp'+n, name:'uptake_comp'+n, type: 'text'})))
	row.append($('<td></td>').append($('<input>', {id:'id_uptake_rate'+n, name:'uptake_rate'+n, type: 'text'})))

	// create <select> elements, add to <tr>
	sel_unit_id='id_uptake_unit'+n
	sel_unit_name='uptake_unit'+n
	sel_unit=$("<select>", {id: sel_unit_id, name: sel_unit_name})
	row.append($('<td></td>').append(sel_unit))

	sel_type_id='id_uptake_type'+n
	sel_type_name='uptake_type'+n
	sel_type=$("<select>", {id: sel_type_id, name: sel_type_name})
	row.append($('<td></td>').append(sel_type))

	// add "Add" button
	add_button=$('<input>', {type: 'button', value: 'Remove', id: 'id_rm_uptake'+n, 'class': 'uptake_rm_button'})
	add_button.click(document.editor.remove_uptake)
	row.append($('<td></td>').append(add_button))
	$('#id_uptake_row1').after(row)
	document.editor.uptake_n+=1

	// Can't populate new select until after it's been added to the DOM:
	document.editor.populate_select_iv('#'+sel_unit_id, document.data['secretion_uptake_units'])
	document.editor.populate_select_iv('#'+sel_type_id, document.data['secretion_uptake_types'], 1)
	document.editor.compound_n+=1

	console.log('add_uptake done')
    },

    remove_uptake: function(eventObj) {
	console.log('remove_uptake entered')
	button_id=eventObj.target.id
	n=button_id.split('uptake')[1]
	row_id='#id_uptake_row'+n
	$(row_id).remove()
    },

    populate_select_vv: function(id_sel, list) {
	for (i in list) {
	    val=list[i]
            $(id_sel).append($('<option>', { value: val }).text(val))
 	}	    
    },  

    populate_select_iv: function(id_sel, list, offset) {
	if (typeof(offset) != "number")
	    offset=0
	for (i in list) {
	    val=list[i]
            $(id_sel).append($('<option>', { value: parseInt(i)+offset }).text(val))
	    console.log('iv: value='+parseInt(i)+offset+', text='+val)
 	}	    
    },  




    prevent_submission: function() {
        console.log('ha ha')
	return false 
    }, 

    allow_submission: function() {
        console.log('away we go')
        return true
    }, 

    submit: function(eventObj) {
	// open the gate, allow submission, and close the gate:
	console.log('submit: about to unbind')
	$('#id_growthdata_form').unbind('submit')
	console.log('submit: about to call submit')
	$('#id_growthdata_form').submit()
	console.log('submit: about to re-close the gate')
	$('#id_growthdata_form').submit(document.editor.prevent_submission)
    },  
}

$(document).ready(function() {
    editor=new GrowthDataEditor() // needs to be moved to <head>?
    document.editor=editor
    editor.push_init_func(editor.init_callbacks,[])
    editor.init()
})
