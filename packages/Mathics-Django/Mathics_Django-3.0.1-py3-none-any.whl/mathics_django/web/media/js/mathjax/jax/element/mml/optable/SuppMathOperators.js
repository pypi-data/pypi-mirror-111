/*
 *  /MathJax-v2/jax/element/mml/optable/SuppMathOperators.js
 *
 *  Copyright (c) 2009-2018 The MathJax Consortium
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

(function(a){var c=a.mo.OPTYPES;var b=a.TEXCLASS;MathJax.Hub.Insert(a.mo.prototype,{OPTABLE:{prefix:{"\u2A03":c.OP,"\u2A05":c.OP,"\u2A07":c.OP,"\u2A08":c.OP,"\u2A09":c.OP,"\u2A0A":c.OP,"\u2A0B":c.INTEGRAL2,"\u2A0C":c.INTEGRAL,"\u2A0D":c.INTEGRAL2,"\u2A0E":c.INTEGRAL2,"\u2A0F":c.INTEGRAL2,"\u2A10":c.OP,"\u2A11":c.OP,"\u2A12":c.OP,"\u2A13":c.OP,"\u2A14":c.OP,"\u2A15":c.INTEGRAL2,"\u2A16":c.INTEGRAL2,"\u2A17":c.INTEGRAL2,"\u2A18":c.INTEGRAL2,"\u2A19":c.INTEGRAL2,"\u2A1A":c.INTEGRAL2,"\u2A1B":c.INTEGRAL2,"\u2A1C":c.INTEGRAL2,"\u2AFC":c.OP,"\u2AFF":c.OP},infix:{"\u2A1D":c.BIN3,"\u2A1E":c.BIN3,"\u2A1F":c.BIN3,"\u2A20":c.BIN3,"\u2A21":c.BIN3,"\u2A22":c.BIN4,"\u2A23":c.BIN4,"\u2A24":c.BIN4,"\u2A25":c.BIN4,"\u2A26":c.BIN4,"\u2A27":c.BIN4,"\u2A28":c.BIN4,"\u2A29":c.BIN4,"\u2A2A":c.BIN4,"\u2A2B":c.BIN4,"\u2A2C":c.BIN4,"\u2A2D":c.BIN4,"\u2A2E":c.BIN4,"\u2A30":c.BIN4,"\u2A31":c.BIN4,"\u2A32":c.BIN4,"\u2A33":c.BIN4,"\u2A34":c.BIN4,"\u2A35":c.BIN4,"\u2A36":c.BIN4,"\u2A37":c.BIN4,"\u2A38":c.BIN4,"\u2A39":c.BIN4,"\u2A3A":c.BIN4,"\u2A3B":c.BIN4,"\u2A3C":c.BIN4,"\u2A3D":c.BIN4,"\u2A3E":c.BIN4,"\u2A40":c.BIN4,"\u2A41":c.BIN4,"\u2A42":c.BIN4,"\u2A43":c.BIN4,"\u2A44":c.BIN4,"\u2A45":c.BIN4,"\u2A46":c.BIN4,"\u2A47":c.BIN4,"\u2A48":c.BIN4,"\u2A49":c.BIN4,"\u2A4A":c.BIN4,"\u2A4B":c.BIN4,"\u2A4C":c.BIN4,"\u2A4D":c.BIN4,"\u2A4E":c.BIN4,"\u2A4F":c.BIN4,"\u2A50":c.BIN4,"\u2A51":c.BIN4,"\u2A52":c.BIN4,"\u2A53":c.BIN4,"\u2A54":c.BIN4,"\u2A55":c.BIN4,"\u2A56":c.BIN4,"\u2A57":c.BIN4,"\u2A58":c.BIN4,"\u2A59":c.REL,"\u2A5A":c.BIN4,"\u2A5B":c.BIN4,"\u2A5C":c.BIN4,"\u2A5D":c.BIN4,"\u2A5E":c.BIN4,"\u2A5F":c.BIN4,"\u2A60":c.BIN4,"\u2A61":c.BIN4,"\u2A62":c.BIN4,"\u2A63":c.BIN4,"\u2A64":c.BIN4,"\u2A65":c.BIN4,"\u2A66":c.REL,"\u2A67":c.REL,"\u2A68":c.REL,"\u2A69":c.REL,"\u2A6A":c.REL,"\u2A6B":c.REL,"\u2A6C":c.REL,"\u2A6D":c.REL,"\u2A6E":c.REL,"\u2A6F":c.REL,"\u2A70":c.REL,"\u2A71":c.BIN4,"\u2A72":c.BIN4,"\u2A73":c.REL,"\u2A74":c.REL,"\u2A75":c.REL,"\u2A76":c.REL,"\u2A77":c.REL,"\u2A78":c.REL,"\u2A79":c.REL,"\u2A7A":c.REL,"\u2A7B":c.REL,"\u2A7C":c.REL,"\u2A7D":c.REL,"\u2A7D\u0338":c.REL,"\u2A7E":c.REL,"\u2A7E\u0338":c.REL,"\u2A7F":c.REL,"\u2A80":c.REL,"\u2A81":c.REL,"\u2A82":c.REL,"\u2A83":c.REL,"\u2A84":c.REL,"\u2A85":c.REL,"\u2A86":c.REL,"\u2A87":c.REL,"\u2A88":c.REL,"\u2A89":c.REL,"\u2A8A":c.REL,"\u2A8B":c.REL,"\u2A8C":c.REL,"\u2A8D":c.REL,"\u2A8E":c.REL,"\u2A8F":c.REL,"\u2A90":c.REL,"\u2A91":c.REL,"\u2A92":c.REL,"\u2A93":c.REL,"\u2A94":c.REL,"\u2A95":c.REL,"\u2A96":c.REL,"\u2A97":c.REL,"\u2A98":c.REL,"\u2A99":c.REL,"\u2A9A":c.REL,"\u2A9B":c.REL,"\u2A9C":c.REL,"\u2A9D":c.REL,"\u2A9E":c.REL,"\u2A9F":c.REL,"\u2AA0":c.REL,"\u2AA1":c.REL,"\u2AA1\u0338":c.REL,"\u2AA2":c.REL,"\u2AA2\u0338":c.REL,"\u2AA3":c.REL,"\u2AA4":c.REL,"\u2AA5":c.REL,"\u2AA6":c.REL,"\u2AA7":c.REL,"\u2AA8":c.REL,"\u2AA9":c.REL,"\u2AAA":c.REL,"\u2AAB":c.REL,"\u2AAC":c.REL,"\u2AAD":c.REL,"\u2AAE":c.REL,"\u2AAF\u0338":c.REL,"\u2AB0\u0338":c.REL,"\u2AB1":c.REL,"\u2AB2":c.REL,"\u2AB3":c.REL,"\u2AB4":c.REL,"\u2AB5":c.REL,"\u2AB6":c.REL,"\u2AB7":c.REL,"\u2AB8":c.REL,"\u2AB9":c.REL,"\u2ABA":c.REL,"\u2ABB":c.REL,"\u2ABC":c.REL,"\u2ABD":c.REL,"\u2ABE":c.REL,"\u2ABF":c.REL,"\u2AC0":c.REL,"\u2AC1":c.REL,"\u2AC2":c.REL,"\u2AC3":c.REL,"\u2AC4":c.REL,"\u2AC5":c.REL,"\u2AC6":c.REL,"\u2AC7":c.REL,"\u2AC8":c.REL,"\u2AC9":c.REL,"\u2ACA":c.REL,"\u2ACB":c.REL,"\u2ACC":c.REL,"\u2ACD":c.REL,"\u2ACE":c.REL,"\u2ACF":c.REL,"\u2AD0":c.REL,"\u2AD1":c.REL,"\u2AD2":c.REL,"\u2AD3":c.REL,"\u2AD4":c.REL,"\u2AD5":c.REL,"\u2AD6":c.REL,"\u2AD7":c.REL,"\u2AD8":c.REL,"\u2AD9":c.REL,"\u2ADA":c.REL,"\u2ADB":c.REL,"\u2ADC":c.REL,"\u2ADD":c.REL,"\u2ADE":c.REL,"\u2ADF":c.REL,"\u2AE0":c.REL,"\u2AE1":c.REL,"\u2AE2":c.REL,"\u2AE3":c.REL,"\u2AE4":c.REL,"\u2AE5":c.REL,"\u2AE6":c.REL,"\u2AE7":c.REL,"\u2AE8":c.REL,"\u2AE9":c.REL,"\u2AEA":c.REL,"\u2AEB":c.REL,"\u2AEC":c.REL,"\u2AED":c.REL,"\u2AEE":c.REL,"\u2AEF":c.REL,"\u2AF0":c.REL,"\u2AF1":c.REL,"\u2AF2":c.REL,"\u2AF3":c.REL,"\u2AF4":c.BIN4,"\u2AF5":c.BIN4,"\u2AF6":c.BIN4,"\u2AF7":c.REL,"\u2AF8":c.REL,"\u2AF9":c.REL,"\u2AFA":c.REL,"\u2AFB":c.BIN4,"\u2AFD":c.BIN4,"\u2AFE":c.BIN3}}});MathJax.Ajax.loadComplete(a.optableDir+"/SuppMathOperators.js")})(MathJax.ElementJax.mml);
