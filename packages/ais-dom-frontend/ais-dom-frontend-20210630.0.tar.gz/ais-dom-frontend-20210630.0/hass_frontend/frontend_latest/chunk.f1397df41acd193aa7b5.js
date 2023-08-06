(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[6334],{84627:(e,o,t)=>{"use strict";t.d(o,{T:()=>n});const i=/^(\w+)\.(\w+)$/,n=e=>i.test(e)},85415:(e,o,t)=>{"use strict";t.d(o,{q:()=>i,w:()=>n});const i=(e,o)=>e<o?-1:e>o?1:0,n=(e,o)=>i(e.toLowerCase(),o.toLowerCase())},73728:(e,o,t)=>{"use strict";t.d(o,{pV:()=>a,P3:()=>r,Ky:()=>l,D4:()=>d,XO:()=>p,zO:()=>h,oi:()=>f,d4:()=>w,D7:()=>g,ZJ:()=>m,V3:()=>_,WW:()=>y});var i=t(95282),n=t(38346),s=t(5986);const a=["unignore","dhcp","homekit","ssdp","zeroconf","discovery","mqtt","hassio"],r=["reauth"],c={"HA-Frontend-Base":`${location.protocol}//${location.host}`},l=(e,o)=>{var t;return e.callApi("POST","config/config_entries/flow",{handler:o,show_advanced_options:Boolean(null===(t=e.userData)||void 0===t?void 0:t.showAdvanced)},c)},d=(e,o)=>e.callApi("GET",`config/config_entries/flow/${o}`,void 0,c),p=(e,o,t)=>e.callApi("POST",`config/config_entries/flow/${o}`,t,c),h=(e,o,t)=>e.callWS({type:"config_entries/ignore_flow",flow_id:o,title:t}),f=(e,o)=>e.callApi("DELETE",`config/config_entries/flow/${o}`),w=e=>e.callApi("GET","config/config_entries/flow_handlers"),g=e=>e.sendMessagePromise({type:"config_entries/flow/progress"}),u=(e,o)=>e.subscribeEvents((0,n.D)((()=>g(e).then((e=>o.setState(e,!0)))),500,!0),"config_entry_discovered"),m=e=>(0,i._)(e,"_configFlowProgress",g,u),_=(e,o)=>m(e.connection).subscribe(o),y=(e,o)=>{const t=o.context.title_placeholders||{},i=Object.keys(t);if(0===i.length)return(0,s.Lh)(e,o.handler);const n=[];return i.forEach((e=>{n.push(e),n.push(t[e])})),e(`component.${o.handler}.config.flow_title`,...n)}},2852:(e,o,t)=>{"use strict";t.d(o,{t:()=>c});var i=t(50424),n=t(85415),s=t(73728),a=t(5986),r=t(52871);const c=(e,o)=>(0,r.w)(e,o,{loadDevicesAndAreas:!0,getFlowHandlers:async e=>{const[o]=await Promise.all([(0,s.d4)(e),e.loadBackendTranslation("title",void 0,!0)]);return o.sort(((o,t)=>(0,n.w)((0,a.Lh)(e.localize,o),(0,a.Lh)(e.localize,t))))},createFlow:async(e,o)=>{const[t]=await Promise.all([(0,s.Ky)(e,o),e.loadBackendTranslation("config",o)]);return t},fetchFlow:async(e,o)=>{const t=await(0,s.D4)(e,o);return await e.loadBackendTranslation("config",t.handler),t},handleFlowStep:s.XO,deleteFlow:s.oi,renderAbortDescription(e,o){const t=e.localize(`component.${o.handler}.config.abort.${o.reason}`,o.description_placeholders);return t?i.dy`
            <ha-markdown allowsvg breaks .content=${t}></ha-markdown>
          `:""},renderShowFormStepHeader:(e,o)=>e.localize(`component.${o.handler}.config.step.${o.step_id}.title`)||e.localize(`component.${o.handler}.title`),renderShowFormStepDescription(e,o){const t=e.localize(`component.${o.handler}.config.step.${o.step_id}.description`,o.description_placeholders);return t?i.dy`
            <ha-markdown allowsvg breaks .content=${t}></ha-markdown>
          `:""},renderShowFormStepFieldLabel:(e,o,t)=>e.localize(`component.${o.handler}.config.step.${o.step_id}.data.${t.name}`),renderShowFormStepFieldError:(e,o,t)=>e.localize(`component.${o.handler}.config.error.${t}`,o.description_placeholders),renderExternalStepHeader:(e,o)=>e.localize(`component.${o.handler}.config.step.${o.step_id}.title`)||e.localize("ui.panel.config.integrations.config_flow.external_step.open_site"),renderExternalStepDescription(e,o){const t=e.localize(`component.${o.handler}.config.${o.step_id}.description`,o.description_placeholders);return i.dy`
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.external_step.description")}
        </p>
        ${t?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${t}
              ></ha-markdown>
            `:""}
      `},renderCreateEntryDescription(e,o){const t=e.localize(`component.${o.handler}.config.create_entry.${o.description||"default"}`,o.description_placeholders);return i.dy`
        ${t?i.dy`
              <ha-markdown
                allowsvg
                breaks
                .content=${t}
              ></ha-markdown>
            `:""}
        <p>
          ${e.localize("ui.panel.config.integrations.config_flow.created_config","name",o.title)}
        </p>
      `},renderShowFormProgressHeader:(e,o)=>e.localize(`component.${o.handler}.config.step.${o.step_id}.title`)||e.localize(`component.${o.handler}.title`),renderShowFormProgressDescription(e,o){const t=e.localize(`component.${o.handler}.config.progress.${o.progress_action}`,o.description_placeholders);return t?i.dy`
            <ha-markdown allowsvg breaks .content=${t}></ha-markdown>
          `:""}})},52871:(e,o,t)=>{"use strict";t.d(o,{w:()=>s});var i=t(47181);const n=()=>Promise.all([t.e(5009),t.e(8161),t.e(2955),t.e(8200),t.e(879),t.e(3967),t.e(1041),t.e(1657),t.e(5829),t.e(1480),t.e(7024),t.e(2374),t.e(6509),t.e(8331),t.e(8101),t.e(4940),t.e(91),t.e(3258)]).then(t.bind(t,27234)),s=(e,o,t)=>{(0,i.B)(e,"show-dialog",{dialogTag:"dialog-data-entry-flow",dialogImport:n,dialogParams:{...o,flowConfig:t}})}},86334:(e,o,t)=>{"use strict";t.r(o);t(53268),t(12730);var i=t(50856),n=t(28426),s=(t(60010),t(38353),t(63081),t(2852)),a=t(47181),r=t(90271);class c extends n.H3{static get template(){return i.d`
      <style include="iron-flex ha-style">
        .content {
          padding-bottom: 32px;
        }
        .border {
          margin: 32px auto 0;
          border-bottom: 1px solid rgba(0, 0, 0, 0.12);
          max-width: 1040px;
        }
        .narrow .border {
          max-width: 640px;
        }
        div.aisInfoRow {
          display: inline-block;
        }
        .center-container {
          @apply --layout-vertical;
          @apply --layout-center-center;
          height: 70px;
        }
        ha-icon-button {
          vertical-align: middle;
        }
      </style>

      <hass-subpage header="Konfiguracja bramki AIS dom">
        <div class$="[[computeClasses(isWide)]]">
          <ha-config-section is-wide="[[isWide]]">
            <span slot="header">Połączenie WiFi</span>
            <span slot="introduction"
              >Możesz sprawdzić lub skonfigurować parametry połączenia
              WiFi</span
            >
            <ha-card header="Parametry sieci">
              <div class="card-content" style="display: flex;">
                <div style="text-align: center;">
                  <div class="aisInfoRow">Lokalna nazwa hosta</div>
                  <div class="aisInfoRow">
                    <mwc-button on-click="showLocalIpInfo"
                      >[[aisLocalHostName]]</mwc-button
                    ><ha-icon-button
                      class="user-button"
                      icon="hass:cog"
                      on-click="createFlowHostName"
                    ></ha-icon-button>
                  </div>
                </div>
                <div on-click="showLocalIpInfo" style="text-align: center;">
                  <div class="aisInfoRow">Lokalny adres IP</div>
                  <div class="aisInfoRow">
                    <mwc-button>[[aisLocalIP]]</mwc-button>
                  </div>
                </div>
                <div on-click="showWiFiSpeedInfo" style="text-align: center;">
                  <div class="aisInfoRow">Prędkość połączenia WiFi</div>
                  <div class="aisInfoRow">
                    <mwc-button>[[aisWiFiSpeed]]</mwc-button>
                  </div>
                </div>
              </div>
              <div class="card-actions">
                <div>
                  <ha-icon-button
                    class="user-button"
                    icon="hass:wifi"
                    on-click="showWiFiGroup"
                  ></ha-icon-button
                  ><mwc-button on-click="createFlowWifi"
                    >Konfigurator połączenia z siecą WiFi</mwc-button
                  >
                </div>
              </div>
            </ha-card>
          </ha-config-section>
        </div>
      </hass-subpage>
    `}static get properties(){return{hass:Object,isWide:Boolean,showAdvanced:Boolean,aisLocalHostName:{type:String,computed:"_computeAisLocalHostName(hass)"},aisLocalIP:{type:String,computed:"_computeAisLocalIP(hass)"},aisWiFiSpeed:{type:String,computed:"_computeAisWiFiSpeed(hass)"},_config:Object,_names:Object,_entities:Array,_cacheConfig:Object}}computeClasses(e){return e?"content":"content narrow"}_computeAisLocalHostName(e){return e.states["sensor.local_host_name"].state}_computeAisLocalIP(e){return e.states["sensor.internal_ip_address"].state}_computeAisWiFiSpeed(e){return e.states["sensor.ais_wifi_service_current_network_info"].state}showWiFiGroup(){(0,a.B)(this,"hass-more-info",{entityId:"group.internet_status"})}showWiFiSpeedInfo(){(0,a.B)(this,"hass-more-info",{entityId:"sensor.ais_wifi_service_current_network_info"})}showLocalIpInfo(){(0,a.B)(this,"hass-more-info",{entityId:"sensor.internal_ip_address"})}_continueFlow(e){(0,s.t)(this,{continueFlowId:e,dialogClosedCallback:()=>{console.log("OK")}})}createFlowHostName(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_host"}).then((e=>{this._continueFlow(e.flow_id)}))}createFlowWifi(){this.hass.callApi("POST","config/config_entries/flow",{handler:"ais_wifi_service"}).then((e=>{console.log(e),this._continueFlow(e.flow_id)}))}ready(){super.ready();const e=(0,r.A)(["sensor.ais_wifi_service_current_network_info"]),o=[],t={};for(const i of e)o.push(i.entity),i.name&&(t[i.entity]=i.name);this.setProperties({_cacheConfig:{cacheKey:o.join(),hoursToShow:24,refresh:0},_entities:o,_names:t})}}customElements.define("ha-config-ais-dom-config-wifi",c)},90271:(e,o,t)=>{"use strict";t.d(o,{A:()=>n});var i=t(84627);const n=e=>{if(!e||!Array.isArray(e))throw new Error("Entities need to be an array");return e.map(((e,o)=>{if("object"==typeof e&&!Array.isArray(e)&&e.type)return e;let t;if("string"==typeof e)t={entity:e};else{if("object"!=typeof e||Array.isArray(e))throw new Error(`Invalid entity specified at position ${o}.`);if(!("entity"in e))throw new Error(`Entity object at position ${o} is missing entity field.`);t=e}if(!(0,i.T)(t.entity))throw new Error(`Invalid entity ID at position ${o}: ${t.entity}`);return t}))}}}]);
//# sourceMappingURL=chunk.f1397df41acd193aa7b5.js.map