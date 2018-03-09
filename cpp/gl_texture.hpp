/***************************************************************************************
 * This code is taken directly from NanoGUI example1.cpp:                              *
 *                                                                                     *
 *     https://github.com/wjakob/nanogui/blob/master/src/example1.cpp                  *
 *                                                                                     *
 * Copyright (c) 2017 Wenzel Jakob <wenzel.jakob@epfl.ch>, All rights reserved.        *
 *                                                                                     *
 * Redistribution and use in source and binary forms, with or without                  *
 * modification, are permitted provided that the following conditions are met:         *
 *                                                                                     *
 * 1. Redistributions of source code must retain the above copyright notice, this      *
 *    list of conditions and the following disclaimer.                                 *
 *                                                                                     *
 * 2. Redistributions in binary form must reproduce the above copyright notice,        *
 *    this list of conditions and the following disclaimer in the documentation        *
 *    and/or other materials provided with the distribution.                           *
 *                                                                                     *
 * 3. Neither the name of the copyright holder nor the names of its contributors       *
 *    may be used to endorse or promote products derived from this software            *
 *    without specific prior written permission.                                       *
 *                                                                                     *
 * THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND     *
 * ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED       *
 * WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE              *
 * DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE        *
 * FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL          *
 * DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR          *
 * SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER          *
 * CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,       *
 * OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE       *
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.                *
 *                                                                                     *
 * You are under no obligation whatsoever to provide any bug fixes, patches, or        *
 * upgrades to the features, functionality or performance of the source code           *
 * ("Enhancements") to anyone; however, if you choose to make your Enhancements        *
 * available either publicly, or directly to the author of this software, without      *
 * imposing a separate written license agreement for such Enhancements, then you       *
 * hereby grant the following license: a non-exclusive, royalty-free perpetual         *
 * license to install, use, modify, prepare derivative works, incorporate into         *
 * other computer software, distribute, and sublicense such enhancements or            *
 * derivative works thereof, in binary and source code form.                           *
 **************************************************************************************/
#pragma once

#include <nanogui/opengl.h>

#define STB_IMAGE_IMPLEMENTATION
#include <stb_image.h>

#include <memory>

class GLTexture {
public:
    using handleType = std::unique_ptr<uint8_t[], void(*)(void*)>;
    GLTexture() = default;
    GLTexture(const std::string& textureName)
        : mTextureName(textureName), mTextureId(0) {}

    GLTexture(const std::string& textureName, GLint textureId)
        : mTextureName(textureName), mTextureId(textureId) {}

    GLTexture(const GLTexture& other) = delete;
    GLTexture(GLTexture&& other) noexcept
        : mTextureName(std::move(other.mTextureName)),
        mTextureId(other.mTextureId) {
        other.mTextureId = 0;
    }
    GLTexture& operator=(const GLTexture& other) = delete;
    GLTexture& operator=(GLTexture&& other) noexcept {
        mTextureName = std::move(other.mTextureName);
        std::swap(mTextureId, other.mTextureId);
        return *this;
    }
    ~GLTexture() noexcept {
        if (mTextureId)
            glDeleteTextures(1, &mTextureId);
    }

    GLuint texture() const { return mTextureId; }
    const std::string& textureName() const { return mTextureName; }

    /**
    *  Load a file in memory and create an OpenGL texture.
    *  Returns a handle type (an std::unique_ptr) to the loaded pixels.
    */
    handleType load(const std::string& fileName) {
        if (mTextureId) {
            glDeleteTextures(1, &mTextureId);
            mTextureId = 0;
        }
        int force_channels = 0;
        int w, h, n;
        handleType textureData(stbi_load(fileName.c_str(), &w, &h, &n, force_channels), stbi_image_free);
        if (!textureData)
            throw std::invalid_argument("Could not load texture data from file " + fileName);
        glGenTextures(1, &mTextureId);
        glBindTexture(GL_TEXTURE_2D, mTextureId);
        GLint internalFormat;
        GLint format;
        switch (n) {
            case 1: internalFormat = GL_R8; format = GL_RED; break;
            case 2: internalFormat = GL_RG8; format = GL_RG; break;
            case 3: internalFormat = GL_RGB8; format = GL_RGB; break;
            case 4: internalFormat = GL_RGBA8; format = GL_RGBA; break;
            default: internalFormat = 0; format = 0; break;
        }
        glTexImage2D(GL_TEXTURE_2D, 0, internalFormat, w, h, 0, format, GL_UNSIGNED_BYTE, textureData.get());
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        return textureData;
    }

private:
    std::string mTextureName;
    GLuint mTextureId;
};

void loadTexture(const std::string &path, std::vector<std::pair<GLTexture, GLTexture::handleType>> &imagesData) {
    GLTexture texture;
    auto data = texture.load(path);
    imagesData.emplace_back(std::move(texture), std::move(data));
}
