
const e = React.createElement;

const {
    Radio,
    Switch,

    Chip,

    Alert,
    AlertTitle,

    Divider,

    Card,
    CardContent,

    Button,

    FormLabel,
    FormControl,
    RadioGroup,
    FormControlLabel,

    Accordion,
    AccordionSummary,
    AccordionDetails,
    ExpandMoreIcon,
    AccordionActions,

    colors,
    CssBaseline,
    ThemeProvider,
    Typography,
    Container,
    makeStyles,
    createMuiTheme,
    Box,
    SvgIcon,
    Link,
    
} = MaterialUI;




class PluginStatus extends React.Component {

    constructor(props) {
        super(props)
        this.state = { 
          url_plugins: window.location.origin + "/plugins",
          plugin_status: {}
        }

    }

    async componentDidMount() {
      
      try {
          const r_value = await axios.get( this.state.url_plugins )

          console.log("data r_value", r_value, Object.keys(r_value).length )
          this.setState( { plugin_status: r_value } )
    
      } catch (error) {
          console.log("EERRR", error)
          // this.setState({com_error: true})
      }
    }


    renderPluginStatusChip(status) {
      if(status=="RUNNING")
      {
        return (<Chip label="Running" className="plugin_running" />)
      }
      else if(status=="STANDBY")
      {
        return (<Chip label="Standby" />)
      }
      else if(status=="WARNING")
      {
        return (<Chip label="Warning" className="plugin_warning" />)
      }
      else if(status=="ERROR")
      {
        return (<Chip label="Error" className="plugin_error" />)
      }
    }

    render() {
        return(<div>
            {
              Object.keys(this.state.plugin_status).map((value, i) => {
                const plugin = this.state.plugin_status[value]

                return (
                  <Accordion key={i}>
                      <AccordionSummary
                        aria-controls="panel1a-content"
                        className="accordion_summary"
                        >
                          { this.renderPluginStatusChip(plugin.status) }
                          <Typography className="accordion_summary_typo"> {value} </Typography>
                          
                      </AccordionSummary>
                      <AccordionDetails>
                        <Typography>
                          {plugin.error_string}
                        </Typography>
                      </AccordionDetails>
                      <Divider />

                      {/* <AccordionActions>
                        <Button size="small">
                          Configure
                        </Button>
                      </AccordionActions> */}

                  </Accordion>
                )
              })
            }
        </div>)
    }

}
