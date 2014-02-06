console.log('hi from new_sources.js')
function efetch_pmid(evt) {
        evt.preventDefault()
        pmid=$('#id_pubmed_id').val()
	if (!pmid.match(/\w+/)) { return false; }
        try {
	url='/defined_media/api/pmid/'+pmid
	console.log('hitting '+url)
	settings={
	    success: function(data, textStatus, jqXHR) {
	        $('#id_first_author').val(data['author'])       
	        $('#id_title').val(data['title'])       
	        $('#id_journal').val(data['journal'])       
	        $('#id_year').val(data['year'])       
	        $('#id_link').val(data['link'])       
		return false
	    },
	    error: function(jqXHR, textStatus, errorThrown) {
	        msg='No article with pubmed id '+pmid+' could be found'
		alert(msg)
//	        throw 'efetch_pmid: '+textStatus+'('+errorThrown+')'
	    },
	}
	$.ajax(url, settings)
	} catch(err) {
   	    console.log('caught error: '+err)
	}
	return false
    }

function submit(eventObj) {
	$('#id_source_form').unbind('submit')
	$('#id_source_form').submit()
	$('#id_source_form').submit(function() { return false })
    }  


$(document).ready(function() {
  // set callbacks
  $('#id_pubmed_id').change(efetch_pmid)
  $('#id_submit_button').click(submit)
})
