GrowthDataEditor=function(o) {
    this.init_funcs=[]
    this.urlmap={}
    this.urlmap_url='/defined_media/api/urlmap'
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
//	$('#id_growthdata_form').submit(document.editor.prevent_submission)
	$('#id_submit_button').click(document.editor.submit)
    },


    //
    // MediaName autocomplete
    // 

    fetch_medianames : function() {
	editor=document.editor
	// fetch all medianames from server
	settings={
	    success: function(media_list, textStatus, jqXHR) {
		     editor.set_medianames_autocomplete(media_list)
		     // more to come?
	    },
	    error: function(jqXHR, textStatus, errorThrown) {
	        throw 'fetch_medianames: '+textStatus+'('+errorThrown+')'
	    },
	}
	$.ajax(editor.urlmap['medianames_api'], settings)
    },

    set_medianames_autocomplete : function(media_list) {
        console.log('got here')
        // use the keys of editor.source_index to initialize autocomplete for #id_sourceid
	var mkeys=[]
	for (i in media_list) {
	    mkeys.push(media_list[i].media_name)
//	    console.log('pushed media_name '+media_list[i]['media_name'])
	}
	console.log(mkeys.length+' keys from server')

      $("#id_media_names").autocomplete({source: mkeys, minLength: 1})
      // this ain't working
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
	$('#id_growthdata_form').unbind('submit')
	$('#id_growthdata_form').submit()
	$('#id_growthdata_form').submit(document.editor.prevent_submission)
    },  
}

$(document).ready(function() {
    editor=new GrowthDataEditor() // needs to be moved to <head>?
    document.editor=editor
    editor.push_init_func(editor.fetch_medianames,[])
    editor.push_init_func(editor.init_callbacks,[])
    editor.init()
})
