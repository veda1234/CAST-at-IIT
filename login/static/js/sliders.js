function plot () {
    console.log('Begin Plot');

		// new code
    let scatterplot_fits = document.getElementById('scatterplot_fits').value || 'default',
      parameters = document.getElementById('parameters').value || 'default';

    console.log(scatterplot_fits, parameters);

    axios.post('/scatter', {
    	scatterplot_fits,
      parameters
    }).then(({data}) => {
    	// check if the data is in correct format
    	console.log(data);

      // if data is in correct format, plot it.
    	Plotly.newPlot('year_histogram', data);
    });
}


$('#scatterplot_fits').on('change', () => plot());
$('#parameters').on('change', () => plot());