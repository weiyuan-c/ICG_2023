const GouraudFragmentShader = `
#extension GL_OES_standard_derivatives : enable 

precision mediump float;

varying vec3 vertexColor;
varying vec3 fragPosition;
varying vec3 fragNormal;
varying vec3 lightLocations[3];
varying vec3 lightColors[3];
varying vec3 lightKdKsCDs[3];
varying float Ka_val;
varying vec3 ambient_lightColor;

varying vec4 fragcolor;   // for gouraud shading

void main(void) {
    gl_FragColor = fragcolor;
}
`;