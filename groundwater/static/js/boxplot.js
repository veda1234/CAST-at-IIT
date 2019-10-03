$('#third_cat').on('change',function(){

    $.ajax({
        url: "/box",
        type: "GET",
        contentType: 'application/json;charset=UTF-8',
        data: {
            'selected': document.getElementById('third_cat').value

        },
        dataType:"json",
        success: function (data) {
            Plotly.newPlot('boxplot', data, data['layout'],{responsive:true} );
        }
    });
})
