var testSexagesimal = /^[+-]?\d+:\d+:\d+(\.\d+)?$/;
var targetData = [];

function setup() {
  $('#generate').click(function() {
    var input = $("textarea[name='coords']").val().split('\n').filter(l => l.length > 0);

    $('#error').html('');
    $('#thumbrow').empty();

    if (input.length % 4 != 0) {
      $('#error').html('Input data must specify four lines per target');
      return;
    }

    targets = [];
    for (var i = 0; i < input.length / 4; i++) {

      var name = input[4*i];
      var tle1 = input[4*i + 1];
      var tle2 = input[4*i + 2];
      var date = input[4*i + 3];

      if (tle1[0] != '1') {
        $('#error').html('Failed to parse "' + tle1 + '" as TLE line 1');
        return;
      }

      if (tle2[0] != '2') {
        $('#error').html('Failed to parse "' + tle2 + '" as TLE line 2');
        return;
      }

      if (isNaN(Date.parse(date))) {
        $('#error').html('Failed to parse "' + date + '" as a date');
        return;
      }

      targets.push({
        'name': name,
        'tle1': tle1,
        'tle2': tle2,
        'date': date
      });
    }
    $('#table').bootstrapTable({columns: [
          {field: 'name', title: 'Name'},
          {field: 'date', title: 'Date'},
          {field: 'ra', title: 'RA'},
          {field: 'dec', title: 'Dec'},
          {field: 'ha', title: 'HA'},
          {field: 'dra', title: 'dRA'},
          {field: 'ddec', title: 'dDec'},
          {field: 'alt', title: 'Alt'},
          {field: 'az', title: 'Az'},
          {field: 'longitude', title: 'Longitude'},
          {field: 'latitude', title: 'Latitude'}]});

    $.ajax ({
      url: generateURL,
      type: "POST",
      data: JSON.stringify(targets),
      dataType: "json",
      contentType: "application/json; charset=utf-8",
      success: function(data){
        $('#table').bootstrapTable("load", data);
      },
      statusCode: {
        500: function() { $('#error').html('Failed to process input'); }
      }
    });
  });
}
