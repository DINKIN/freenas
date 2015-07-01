// Disk Item Icon Component
// ========================
// Custom icon component for each disk item, to replace the standard ItemIcon

"use strict";

import _ from "lodash";
import React from "react";

// Defines which font icon to use as a glyph for each type of disk. These are
// terrible choice on purpose, because we plan to replace them.
const GLYPH_MAP = { HDD: "key"
                  , SSD: "globe"
                  , tapeDrive: "house"
                  };

const DiskItemIcon = React.createClass({

  propTypes: { serial: React.PropTypes.string
             , byteSize: React.PropTypes.number
             , humanSize: React.PropTypes.string
             , online: React.PropTypes.bool
             , path: React.PropTypes.string.isRequired
             , size: React.PropTypes.number
             , fontSize: React.PropTypes.number
             , badgeFontSize: React.PropTypes.number
             , diskType: React.PropTypes.string
             }

  , getDefaultProps: function () {
    return ( { serial: ""
             , byteSize: null
             , humanSize: ""
             , online: null
             , model: ""
             , size: null
             , fontSize: 2
             , badgeFontSize: .6
             , diskType: "HDD"
             }
           );
  }

  , render: function () {
    let iconBadge = null;

    // TODO: support warning badges etc.
    let badgeStyle = "info";

    let iconStyle = {};
    let iconClassName = null;

    if ( this.props.size ) {
      iconStyle.height = this.props.size;
      iconStyle.width = this.props.size;
    }

    if ( this.props.humanSize !== "" ) {
      iconBadge = <span
                    style = { { fontSize: this.props.badgeFontSize + "em" } }>
                    { this.props.humanSize }
                  </span>;
    }

    // Keeping this as a _.without because I expect to add back in nullable
    // values, such as option error styles.
    iconClassName = _.without(
                      [ "fa"
                      , ( "fa-" + GLYPH_MAP[ this.props.diskType ] )
                      , ( "badge-" + badgeStyle )
                      ]
                    , null ).join( " " ) ;

    return (
      <div>
        <div { ...iconStyle } >
          <i className = { iconClassName }
            style = { { fontSize: this.props.fontSize + "em" } } >
            { iconBadge }
          </i>
        </div>
        <div>
          <h6>
            { this.props.path }
          </h6>
        </div>
      </div>
    );
  }

});

export default DiskItemIcon;
