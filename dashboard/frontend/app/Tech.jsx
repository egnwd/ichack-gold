import React from 'react';

class Tech extends React.Component {

    constructor() {
        super();
    }

    loadJSON(filePath) {
        var json = this.loadText(filePath, "application/json");
        return JSON.parse(json);
    }

    loadText(filePath, mimeType) {
      var xmlhttp=new XMLHttpRequest();
      xmlhttp.open("GET",filePath,false);
      if (mimeType != null) {
          if (xmlhttp.overrideMimeType) {
                xmlhttp.overrideMimeType(mimeType);
              }
        }
          xmlhttp.send();
      if (xmlhttp.status==200) {
          return xmlhttp.responseText;
      }
      else {
        return null;
      }
    }

    render() {
        var id = this.props.id;
        let data = this.loadJSON("/static/tech.json");
        let item = data[this.props.idx];
        let tech = item.tech.map((t) => {return (<li>{t}</li>)});
        console.log(tech);
        return (
            <div className="tech-area">
                <h2 className="tk-brothers">{item.name}</h2>
                <ul>
                    {tech}
                </ul>
            </div>
        );
    }

}

export default Tech;
