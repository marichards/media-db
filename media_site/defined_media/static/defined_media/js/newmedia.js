NewMediaEditor=function(o) {
    this.init_funcs=[]
    this.urlmap={}
    this.urlmap_url='/defined_media/api/urlmap'
}

function stackTrace() {
    var err=new Error()
    return err.stack;
}

NewMediaEditor.prototype={
    push_init_func : function(f, args) { this.init_funcs.push([f, args]) },

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
		    init_f.apply(args)
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
	$('#id_genus').change(document.editor.load_species_sel)
	$('#id_species').change(document.editor.load_strain_sel)
	$('#id_add_compound1').click(document.editor.add_compound)
    },

    fetch_organisms : function() {
	editor=document.editor
	// fetch all organisms from server
	settings={
	    success: function(org_list, textStatus, jqXHR) {
		editor.build_org_index(org_list)
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

    compound_n: 1,

    add_compound : function(eventObj) {
	// this is a callback for when an 'Add' button is clicked.
	// It inserts a new compound row into the document.

	// create tr element and three td elements:
	n=document.editor.compound_n+1
	row=$('<tr></tr>', {id: 'id_comp_row'+n})
	row.append($('<td></td>').append($('<input>', {id:'id_comp'+n, name:'comp'+n, type: 'text'})))
	row.append($('<td></td>').append($('<input>', {id:'id_amount'+n, name:'amount'+n, type: 'text'})))

	add_button=$('<input>', {type: 'button', value: 'Remove', id: 'id_rm_compound'+n})
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
    }

}

$(document).ready(function() {
    editor=new NewMediaEditor() // needs to be moved to <head>?
    document.editor=editor
    editor.push_init_func(editor.fetch_organisms)
    editor.push_init_func(editor.init_callbacks)
    editor.init()
})