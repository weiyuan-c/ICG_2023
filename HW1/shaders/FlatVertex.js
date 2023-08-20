const FlatVertexShader = `

attribute vec3 aVertexPosition;
attribute vec3 aFrontColor;
attribute vec3 aVertexNormal;

uniform vec3 lightLoc[3];
uniform vec3 lightColor[3];
uniform vec3 lightKdKsCD[3];
uniform mat4 uMVMatrix;
uniform mat4 uPMatrix;
uniform float Ka;
uniform float Kd;
uniform float Ks;
uniform float Cd;
uniform vec3 ambient_color;

uniform int mode;
uniform float volume;

varying vec3 vertexColor;
varying vec3 fragPosition;
varying vec3 fragNormal;
varying vec3 shading_mode;
varying vec3 lightLocations[3];
varying vec3 lightColors[3];
varying vec3 lightKdKsCDs[3];
varying float Ka_val;
varying float Kd_val;
varying float Ks_val;
varying float Cd_val;
varying vec3 ambient_lightColor;

varying vec3 fragcolor;
varying vec3 mvVertex;

void main(void) {
    Ka_val = Ka;
    Kd_val = Kd;
    Ks_val = Ks;
    Cd_val = Cd;
    ambient_lightColor = ambient_color;
    for(int i=0; i<3 ; ++i){
        lightLocations[i] = lightLoc[i];
        lightColors[i] = lightColor[i];
        lightKdKsCDs[i] = lightKdKsCD[i];
    }

    vec3 vertex_copy = aVertexPosition;
    vertex_copy.x *= 1.+volume;
    vertex_copy.y *= 1.+volume;
    vertex_copy.z *= 1.+volume;

    mvVertex = (uMVMatrix * vec4(vertex_copy, 1.0)).xyz;
    fragcolor = aFrontColor;
    gl_Position = uPMatrix * vec4(mvVertex, 1.0);

}
`;