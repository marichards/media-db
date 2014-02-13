GrowthDataEditor=function(o) {
    this.init_funcs=[]
    this.urlmap={}
    this.urlmap_url='/defined_media/api/urlmap'
    this.secuptake_n=$('.secuptake_rm_button').length+1
    this.uptake_n=$('.uptake_rm_button').length+1
    this.source_visible=0
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

	$('#id_genus').change(document.editor.load_species_sel)
	$('#id_species').change(document.editor.load_strain_sel)

	$('#id_sourceid').change(document.editor.show_full_source)

	// add event handlers for uptake add/rm buttons
 	$('#id_add_secuptake1').click(document.editor.add_secuptake)
	$('.secuptake_rm_button').click(document.editor.remove_secuptake)
    },


    //
    // Dynamic organism selects:
    //

    fetch_organisms : function() {
	editor=document.editor
	// fetch all organisms from server
	settings={
	    success: function(org_list, textStatus, jqXHR) {
		editor.build_org_index(org_list)
//		editor.dump_org_index()
		editor.load_species_sel()
	    },
	    error: function(jqXHR, textStatus, errorThrown) {
	        throw 'fetch_organisms: '+textStatus+'('+errorThrown+')'
	    },
	}
	$.ajax(editor.urlmap['organism_api'], settings)
    },

    build_org_index : function(org_list) {
	org_index={}
	for (i in org_list ) {
	    org=org_list[i]
	    genus=org['genus']
	    species=org['species']
	    strain=org['strain']
	    if (org_index[genus]==undefined) { org_index[genus]={}}
	    if (org_index[genus][species]==undefined) { org_index[genus][species]=[] }
	    org_index[genus][species].push(strain)
	}
	document.editor.org_index=org_index
    },


    load_species_sel : function() {
	genus=$('#id_genus').val()
	$('#id_species').empty()
	species_dict=document.editor.org_index[genus]
	species_sel=$('#id_species')
	to_select=null
	for (species in document.editor.org_index[genus]) {
	    if (to_select==null) to_select=species
	    species_sel.append($('<option>', { value: species }).text(species))
	}
	$('#id_species').val(to_select).change()
    },

    load_strain_sel : function() {
	genus=$('#id_genus').val()
	species=$('#id_species').val()
	strain_list=document.editor.org_index[genus][species]
	strain_sel=$('#id_strain')
	strain_sel.empty()
	for (i in strain_list) {
	    strain=strain_list[i]
	    strain_sel.append($('<option>', { value: strain }).text(strain))
	}
    },

    dump_org_index : function() {
	n=Object.keys(document.editor.org_index).length
	console.log(n+' keys in org_index')
	n_genus=0
	n_species=0
	n_strains=0
	for (genus in document.editor.org_index) {
	    n_genus+=1
	    species_hash=document.editor.org_index[genus]
	    for (species in species_hash) {
		n_species+=1
		n_strains+=species_hash[species].length
	    }
	}
	console.log('n_genus: '+n_genus)
	console.log('n_species: '+n_species)
	console.log('n_strain: '+n_strains)
    }, 

    //
    // Sources autocomplete
    //
    fetch_sources : function() {
	editor=document.editor
	// fetch all sources from server
	settings={
	    success: function(src_list, textStatus, jqXHR) {
	    	     editor.build_sources_index(src_list)
		     editor.set_sources_autocomplete()
		     // more to come?
	    },
	    error: function(jqXHR, textStatus, errorThrown) {
	        throw 'fetch_sources: '+textStatus+'('+errorThrown+')'
	    },
	}
	$.ajax(editor.urlmap['sources_api'], settings)
    },

    build_sources_index : function(src_list) {
        // build an index: k=src.first_author + src.year
	//                 v={first_author: src.first_author, etc (all fields)}
	// put result in editor.source_index
	source_index={}
	for (i in src_list) {
	    src_info=src_list[i]
	    key=src_info['first_author']+' '+src_info['year']
	    source_index[key]=src_info
	}
	document.editor.source_index=source_index
    },

    set_sources_autocomplete : function() {
        // use the keys of editor.source_index to initialize autocomplete for #id_sourceid
	keys=[]
	for (i in document.editor.source_index) {
	    keys.push(i)
	}
	$("#id_sourceid").autocomplete({source: keys, 
	                                change: document.editor.show_full_source,
	})
    },

    show_full_source : function(evt, ui) {
        key=$('#id_sourceid').val()
	src=document.editor.source_index[key]
	if (!src) return
	full_src=src['first_author']+': '+src['title']+' '+src['year']
	$('#id_full_source').text(full_src)
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
        // use the keys of editor.source_index to initialize autocomplete for #id_sourceid
	keys=[]
	for (i in media_list) {
	    keys.push(media_list[i].media_name)
//	    console.log('pushed media_name '+media_list[i]['media_name'])
	}
	console.log(keys.length+' medianames keys')
	$("#id_media_names").autocomplete({source: keys, minLength: 1})
    },

    //
    // SecretionUptake dynamic list:
    //

    add_secuptake : function(eventObj) {
	// this is a callback for when an 'Add' button is clicked.
	// It inserts a new secuptake row into the document.
	console.log('hi from add_secuptake')

	// create tr element and three td elements:
	n=document.editor.secuptake_n+1
	console.log('n is '+n)
	row=$('<tr></tr>', {id: 'id_comp_row'+n})
	row.append($('<td></td>').append($('<input>', {id:'id_comp'+n, name:'comp'+n, type: 'text'})))
	row.append($('<td></td>').append($('<input>', {id:'id_amount'+n, name:'amount'+n, type: 'text'})))

	add_button=$('<input>', {type: 'button', value: 'Remove', id: 'id_rm_secuptake'+n, 'class': 'secuptake_rm_button'})
	add_button.click(document.editor.remove_secuptake)
	row.append($('<td></td>').append(add_button))
	$('#id_comp_row1').after(row)
	document.editor.secuptake_n+=1
	console.log('add_secuptake done')
    },

    remove_secuptake: function(eventObj) {
	console.log('remove_secuptake entered')
	button_id=eventObj.target.id
	n=button_id.split('secuptake')[1]
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
	$('#id_growthdata_form').unbind('submit')
	$('#id_growthdata_form').submit()
	$('#id_growthdata_form').submit(document.editor.prevent_submission)
    },  
}

$(document).ready(function() {
    editor=new GrowthDataEditor() // needs to be moved to <head>?
    document.editor=editor
    editor.push_init_func(editor.fetch_organisms,[])
    editor.push_init_func(editor.fetch_sources,[])
    editor.push_init_func(editor.fetch_medianames,[])
    editor.push_init_func(editor.init_callbacks,[])
    editor.init()
})
