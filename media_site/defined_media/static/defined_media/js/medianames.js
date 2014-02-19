MediaNamesEditor=function(o) {
    this.init_funcs=[]
    this.urlmap={}
    this.urlmap_url='/defined_media/api/urlmap'
    this.compound_n=$('.compound_rm_button').length+1
    this.uptake_n=$('.uptake_rm_button').length+1
    this.source_visible=0
}


MediaNamesEditor.prototype={
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
	$('#id_add_compound1').click(document.editor.add_compound)
	$('#id_newmedia_form').submit(document.editor.prevent_submission)
	$('#id_submit_button').click(document.editor.submit)
	$('.compound_rm_button').click(document.editor.remove_compound)
	// add event handlers for comp and uptake rm buttons
    },


    add_compound : function(eventObj) {
	// this is a callback for when an 'Add' button is clicked.
	// It inserts a new compound row into the document.

	// create tr element and three td elements:
	n=document.editor.compound_n+1
	row=$('<tr></tr>', {id: 'id_comp_row'+n})
	row.append($('<td></td>').append($('<input>', {id:'id_comp'+n, name:'comp'+n, type: 'text'})))
	row.append($('<td></td>').append($('<input>', {id:'id_amount'+n, name:'amount'+n, type: 'text'})))

	add_button=$('<input>', {type: 'button', value: 'Remove', id: 'id_rm_compound'+n, 'class': 'compound_rm_button'})
	add_button.click(document.editor.remove_compound)
	row.append($('<td></td>').append(add_button))
	$('#id_comp_row1').after(row)
	document.editor.compound_n+=1
    },

    remove_compound: function(eventObj) {
	button_id=eventObj.target.id
	n=button_id.split('compound')[1]
	row_id='#id_comp_row'+n
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
 	}	    
    },  

    prevent_submission: function() {
//        console.log('ha ha')
	return false 
    }, 

    allow_submission: function() {
//        console.log('away we go')
        return true
    }, 

    submit: function(eventObj) {
	// open the gate, allow submission, and close the gate:
	$('#id_newmedia_form').unbind('submit')
	$('#id_newmedia_form').submit()
	$('#id_newmedia_form').submit(document.editor.prevent_submission)
    },  
}

$(document).ready(function() {
    editor=new MediaNamesEditor() // needs to be moved to <head>?
    document.editor=editor
    editor.push_init_func(editor.init_callbacks,[])
    editor.init()
})
