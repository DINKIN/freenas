// MACH SERVER
// ES5

"use strict";

// Babel Require hook - transform any ES6 after this point, including through
// the require chain.
// http://babeljs.io/docs/usage/require/
require( "babel/register" );

var fs   = require( "fs" );
var path = require( "path" );
var mach = require( "mach" );
var when = require( "when" );

var React  = require( "react" );
var Router = require( "react-router" );

var routes = require( "./jsx/routes" );

// Content
var jsBundle = fs.readFileSync( __dirname + "/build/js/app.js" );

var app = mach.stack();


// Mach server helpers
function renderApp ( path ) {
  return new when.Promise( function ( resolve, reject ) {
    Router.run( routes, path, function ( Handler ) {
      var pageHTML = React.renderToString( React.createElement( Handler ) );

      if ( pageHTML ) {
        resolve( "<!DOCTYPE html>" + pageHTML );
      } else {
        reject( "Handler for " + path + " did not return any HTML when "
              + "rendered to string"
              );
      }
    });
  });
}

// Mach server config
app.use( mach.gzip );
app.use( mach.favicon );
app.use( mach.file, { root: path.join( __dirname, "build" ) } );

// Routes
app.get( "/js/app.js"
       , function ( request ) {
           return jsBundle;
         }
       );

app.get( "*"
       , function ( request ) {
           return renderApp( request.path );
         }
       );

// Start Mach server
mach.serve( app, ( process.env.PORT || 3000 ) );
