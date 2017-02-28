<html>
  <head>
    <title>pygraphweb</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" integrity="sha384-rwoIResjU2yc3z8GV/NPeZWAv56rSmLldC3R/AZzGRnGxQQKnKkoFVhFQhNUwEyJ" crossorigin="anonymous" />
    <link href="http://cdn.pydata.org/bokeh/release/bokeh-0.12.4.min.css" rel="stylesheet" type="text/css">
    <link href="http://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.4.min.css" rel="stylesheet" type="text/css">
    <script src="https://code.jquery.com/jquery-3.1.1.slim.min.js" integrity="sha384-A7FZj7v+d/sdmMqp/nOQwliLvUsJfDHW+k9Omg/a/EheAdgtzNs3hpfag6Ed950n" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" integrity="sha384-vBWWzlZJ8ea9aCX4pEW3rVHjgjt7zpkNpZk+02D9phzyeVkE+jo0ieGizqPLForn" crossorigin="anonymous"></script>
    <script type="text/javascript" async src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-MML-AM_CHTML"></script>
    <script src="http://cdn.pydata.org/bokeh/release/bokeh-0.12.4.min.js"></script>
    <script src="http://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.4.min.js"></script>
  </head>
  <body>
    <div class="container">
      <div class="row">
        <div class="col-md-12">
          <h1>pygraphweb awaits your commands...</h1>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <form action="/" method="post">
            <div class="row">
              <div class="form-group col-md-9">
                <input class="form-control" id="expression" name="expression" type="text" placeholder="Enter expression..." />
              </div>
              <div class="form-group col-md-3">
                <input class="form-control" id="variables" name="variables" type="text" placeholder="Enter variables..." />
              </div>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Solve for first variable specified and graph result!</button>
          </form>
        </div>
      </div>
      <div class="row">
        <div class="col-md-6">
          <div class="card">
            <div class="card-block">
              <h4 class="card-title">Original expression...</h4>
            </div>
            <div class="card-block">\[{{expression}}\]</div>
          </div>
        </div>
        <div class="col-md-6">
          <div class="card">
            <div class="card-block">
              <h4 class="card-title">...and solved expression!</h4>
            </div>
            <div class="card-block">\[{{solved_expression}}\]</div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="col-md-12">
          <div class="card">
            <div class="card-block">
              {{!div}}
            </div>
          </div>
        </div>
      </div>
    </div>
    {{!script}}
  </body>
</html>
