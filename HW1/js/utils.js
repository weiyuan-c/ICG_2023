class CGObject{
    constructor(id=0, name="", trans_vec=null, rotate_vec=null, scale_vec=null, scale_init=null, shear_vec=null, shader="", Kd=0.6, Ks=0.3, Cd=20.0) {
        
        this.id = id;
        this.Kd = Kd;
        this.Ks = Ks;
        this.CD = Cd;
        this.name = name;
        
        this.VertexPositionBuffer;
        this.VertexNormalBuffer;
        this.VertexFrontColorBuffer;
        this.vertexTextureCoordBuffer;
        
        this.translation_vec = trans_vec;
        this.rotate_vec = rotate_vec;
        this.scale_vec = scale_vec;
        this.scale_init = scale_init;
        this.shear_vec = shear_vec;
        this.shader = shader

        this.mvMatrix = mat4.create();
        this.pMatrix  = mat4.create();
        this.texture  = "NONE";
    }

    set_translation_vec(trans_vec){  this.translation_vec = trans_vec;  }

    set_rotate_vec(rotate_vec){ this.rotate_vec = rotate_vec; }

    set_scale_vec(scale_vec){ this.scale_vec = scale_vec; }

    set_scale_init(scale_init){ this.scale_init = scale_init; }

    set_shear_vec(shear_vec){  this.shear_vec = shear_vec; }

    set_shader(shader){  this.shader = shader; }

    translation(){ mat4.translate(this.mvMatrix, this.translation_vec); }

    rotation(){
        var rx = degToRad(this.rotate_vec[0]);
        mat4.rotate(this.mvMatrix, rx, [1, 0, 0]);

        var ry = degToRad(this.rotate_vec[1]);
        mat4.rotate(this.mvMatrix, ry, [0, 1, 0]);

        var rz = degToRad(this.rotate_vec[2]);
        mat4.rotate(this.mvMatrix, rz, [0, 0, 1]);
    }

    scale(){ mat4.scale(this.mvMatrix, this.scale_vec); }

    shear(){
        var cotx =  1 / Math.tan(degToRad(this.shear_vec[0]));
        var coty =  1 / Math.tan(degToRad(this.shear_vec[1]));
        var cotz =  1 / Math.tan(degToRad(this.shear_vec[2]));
        mat4.multiply(this.mvMatrix, mat4.create([1, 0, cotz, 0, cotx, 1, 0, 0, 0, coty, 1, 0, 0, 0, 0, 1]));
    }
}

class LightObject{
    constructor(position=null, color=null) {
        this.position = position;
        this.color = color;
    }

    set_position(position){
        this.position = position;
    }

    set_color(color){
        this.color = color;
    }
}

class LightArray{
    lights = []
    
    add_light(light){
        this.lights.push(light);
    }

    size(){
        return this.lights.length;
    }

    access_light(idx){
        if(idx >= this.size()){
            throw 'index out of limited.';
        }

        return this.lights[idx];
    }
}