const GouraudVertexShader = `

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

uniform float volume;

varying vec3 vertexColor;
varying vec3 fragPosition;
varying vec3 fragNormal;
varying vec3 shading_mode;
varying vec3 lightLocations[3];
varying vec3 lightColors[3];
varying vec3 lightKdKsCDs[3];
varying float Ka_val;
varying vec3 ambient_lightColor;

varying vec4 fragcolor;

void main(void) {
    Ka_val = Ka;;
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

    vec3 phong = vec3(0.0, 0.0, 0.0);
    vec3 mvVertex = (uMVMatrix * vec4(vertex_copy, 1.0)).xyz;
    vec3 mvNormal = mat3(uMVMatrix) * aVertexNormal;

    float ka = Ka; 
    vec3 V = -normalize(mvVertex);
    vec3 N = normalize(mvNormal);

    vec3 ambient = ka * ambient_lightColor;
    for(int i=0 ; i<3 ; ++i){
        float CosineDegree = lightKdKsCD[0][2];
        vec3 L = normalize(lightLoc[i] - mvVertex);
        vec3 H = normalize(L+V);

        vec3 Id = lightColor[i] * max(dot(L, N), 0.0);
        vec3 diffuse = Kd * Id;

        vec3 Is = lightColor[i] * pow(max(dot(N, L), 0.0), Cd);
        vec3 specular = Ks * Is;

        if(dot(L, N) < 0.){
            specular = vec3(0., 0., 0.);
        }
        phong += aFrontColor * (ambient + diffuse) + specular;
    }
    // phong += ambient * aFrontColor;
    fragcolor = vec4(phong, 1.0);
    gl_Position = uPMatrix * uMVMatrix * vec4(vertex_copy, 1.0);
    
}
`;