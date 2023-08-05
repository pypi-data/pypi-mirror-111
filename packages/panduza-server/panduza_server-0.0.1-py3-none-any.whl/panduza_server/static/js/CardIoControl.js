'use strict';



const e = React.createElement

const {
    Radio,
    Switch,

    Alert,
    AlertTitle,

    Card,
    CardContent,
    Typography,

    FormLabel,
    FormControl,
    RadioGroup,
    FormControlLabel,

} = MaterialUI;



class CardIoControl extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            com_error: false,
            value: "0",
            direction: "in",
            url_io: window.location.origin + "/io/" + this.props.target
        }
        this.handleValueChange = this.handleValueChange.bind(this);
        this.handleDirectionChange = this.handleDirectionChange.bind(this);
    }

    async componentDidMount() {
        // console.log("componentDidMount")
        try {
            const r_value = await axios.get( this.state.url_io + "/value" )
            const r_direction = await axios.get( this.state.url_io + "/direction" )

            console.log("data r_value", r_value.value)
            this.setState({value: r_value.value.toString() })

        
        } catch (error) {
            console.log("EERRR", error)
            this.setState({com_error: true})
        }
    }

    async handleValueChange(r) {
        try {
            const new_value = parseInt(r.target.value)
            await axios.put( this.state.url_io + "/value", { value: new_value } )
            this.setState({value: r.target.value })
        
        } catch (error) {
            console.log("EERRR", error)
            this.setState({com_error: true})
        }
    }


    async handleDirectionChange(r) {
        try {
            console.log("WWW >>> ", r)
            const new_direction = r.target.value
            await axios.put( this.state.url_io + "/direction", { direction: new_direction } )
            this.setState( { direction: new_direction })
        
        } catch (error) {
            console.log("EERRR", error)
            this.setState({com_error: true})
        }
    }

    render() {
        // console.log("RENDER", this.state.com_error)
        if(this.state.com_error) {
            // return e(Switch, {  },  null)
            // return e(Alert, { severity: "error" }, 
            //     "Errororoor"
            // )
            return "ERROR"
        }
        else {    
            return e(Card, { className: "io_card" },
                    e(CardContent, { },
                        e(Typography, { variant:"h5", component:"h2" },
                            "IO " + this.props.target
                        )
                    ),
                    e(FormControl, { component:"fieldset" },
                        e(FormLabel, {component: "legend"}, "Direction"),
                        e(RadioGroup, {
                            value:this.state.direction,
                            onChange:this.handleDirectionChange
                        },
                            e(FormControlLabel, { value:"in", control:e(Radio), label:"Input" }),
                            e(FormControlLabel, { value:"out", control:e(Radio), label:"Ouput" })
                        )
                    ),
                    e(FormControl, { component:"fieldset" },
                        e(FormLabel, {component: "legend"}, "Value"),
                        e(RadioGroup, {
                            value:this.state.value,
                            onChange:this.handleValueChange
                        },
                            e(FormControlLabel, { value:"0", control:e(Radio), label:"0" }),
                            e(FormControlLabel, { value:"1", control:e(Radio), label:"1" })
                        )
                    )
                )
            }
    }


}




