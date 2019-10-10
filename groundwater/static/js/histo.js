function plot () {
    console.log('Begin Plot');

		// new code
    let histogramFeature = document.getElementById('histogramFeature').value || 'default',
      parameter = document.getElementById('parameter').value || 'default';

    console.log(histogramFeature, parameter);

    axios.post('/hist', {
    	histogramFeature,
      parameter
    }).then(({data}) => {
    	// check if the data is in correct format
    	console.log(data);

      // if data is in correct format, plot it.
    	Plotly.newPlot('plot', data,data['layout'],{responsive:true});
    });
}


$('#histogramFeature').on('change', () => plot());
$('#parameter').on('change', () => plot());
